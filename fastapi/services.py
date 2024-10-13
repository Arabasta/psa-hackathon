from datetime import datetime
from firebase_config import db, bucket
import os
import io
import uuid
import random
import logging
import aiofiles
from pathlib import Path
from fastapi import File, UploadFile

logger = logging.getLogger('uvicorn')

async def upload_image_to_storage(image):
    image_name = f"{uuid.uuid4()}_{image.filename}"
    blob = bucket.blob(image_name)
    image_content = await image.read()
    blob.upload_from_string(image_content, content_type=image.content_type)
    blob.make_public()
    return blob.public_url


def store_submission_in_firestore(image_url, image_caption, employees):
    submission_data = {
        "dateTime": datetime.now().isoformat(),
        "imageCaption": image_caption,
        "employees": employees,
        "imageURL": image_url
    }

    doc_ref = db.collection("submissions").add(submission_data)
    doc_id = doc_ref[1].id

    return {"id": doc_id, **submission_data}


def get_submission_from_firestore(image_id):
    doc_ref = db.collection("submissions").document(image_id)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()
    else:
        return None


def get_random_image():
    # get all docs
    doc_list = [doc for doc in db.collection("submissions").stream()]
    if not doc_list:
        return None

    random_doc = random.choice(doc_list)
    return random_doc.to_dict()


def get_next_images(last_image_id=None, limit=5):
    submissions_ref = db.collection("submissions").order_by("dateTime")

    if last_image_id:
        last_image = db.collection("submissions").document(last_image_id).get()
        if last_image.exists:
            submissions_ref = submissions_ref.start_after(last_image)

    docs = submissions_ref.limit(limit).stream()
    images = [doc.to_dict() for doc in docs]

    return images

'''
    1. Retrieve uploaded image
    2. Generate image and keypoints json
    3. Perform OKS scoring
    4. Upload generated image to Storage
    5. Return to React: 1) generated image url for display, 2) OKS score
'''

RAW_IMAGE_DIR = str(Path(__file__).parent)+"/raw_image"
RENDERED_IMAGE_DIR = str(Path(__file__).parent)+"/rendered_image"

async def openpose_handle_new_image(image_name, image: UploadFile = File(...)):
    from main import (get_current_bomen_name, process_raw_image_from_dir, calculate_oks_score)
    from main import Utils

    global RAW_IMAGE_DIR
    global RENDERED_IMAGE_DIR
    generated_image_data = {}
    # try:
    # store image to RAW_IMAGE_DIR
    image_name = os.path.splitext(image.filename)[0]
    await save_upload_file_to_path(RAW_IMAGE_DIR+"/"+image_name+".png", image)
    logger.info("openpose_handle_new_image - image_name: "+image_name)

    if process_raw_image_from_dir(image_name) is False:
        raise Exception("Failed to use OpenPose to process image: "+image_name)

    logger.info("openpose_handle_new_image - getting file path ... "+image_name+"_rendered.png")
    upload_file_path = Utils.get_rendered_image_file_path(image_name)
    logger.info("openpose_handle_new_image - upload_file_path: "+upload_file_path)

    upload_file = await create_upload_file_from_path(upload_file_path)

    generated_image_data["image_url"] = await upload_image_to_storage(upload_file)
    generated_image_data["oks_score"] = calculate_oks_score(image_name)

    # except Exception as e:
    #     logger.error(e)
    #     pass

    return {**generated_image_data}


async def save_upload_file_to_path(out_file_path, in_file: UploadFile=File(...)):
    async with aiofiles.open(out_file_path, 'wb') as out_file:
        while content := await in_file.read(1024):  # async read chunk
            await out_file.write(content)  # async write chunk


async def create_upload_file_from_path(file_path: str) -> UploadFile:
    file_name = os.path.basename(file_path)

    # Open the file asynchronously
    async with aiofiles.open(file_path, "rb") as file:
        # Read the content and create an UploadFile object
        file_content = await file.read()
        upload_file = UploadFile(filename=file_name, file=io.BytesIO(file_content))

    return upload_file
