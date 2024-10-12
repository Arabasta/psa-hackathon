from datetime import datetime
from firebase_config import db, bucket
import uuid
import random


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
