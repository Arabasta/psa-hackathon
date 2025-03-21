from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Query
from services import (upload_image_to_storage, store_submission_in_firestore, get_submission_from_firestore,
                      get_random_image, get_next_image, openpose_handle_new_image, get_bomen_of_the_day)
from typing import List

router = APIRouter()


@router.get("/api/health")
async def health():
    return {"message": "Fastapi Healthy"}


@router.get("/")
async def home():
    return {"message": "Hello, World!"}


@router.post("/api/upload")
async def upload_image(image: UploadFile = File(...), image_caption: str = Form(...), employees: str = Form(...)):
    # resize image
    # image = await resize_image(image)
    image_name = image.filename
    image_url = await upload_image_to_storage(image)

    # store metadata in Firestore
    firestore_submission_data = store_submission_in_firestore(image_url, image_caption, employees)
    # Rewind the file after uploading to storage
    await image.seek(0)
    # activate services.openpose_handle_new_image handle new image, and return URL of generated image and OKS score
    openpose_uploaded_image_data = await openpose_handle_new_image(image_name, image)

    # combines the above 2 dicts together
    submission_data = firestore_submission_data | openpose_uploaded_image_data

    return {"message": "Image uploaded successfully", "data": submission_data}


@router.get("/api/image/{image_id}")
async def get_image_data(image_id: str):
    image_data = get_submission_from_firestore(image_id)

    if not image_data:
        raise HTTPException(status_code=404, detail="Image not found")

    return {"message": "Image retrieved successfully", "data": image_data}


@router.get("/api/random_image")
async def random_image():
    image_data = get_random_image()

    if not image_data:
        raise HTTPException(status_code=404, detail="No images found")

    return {"message": "Random image retrieved successfully", "data": image_data}


@router.get("/api/next_image")
async def next_image(last_image_id: str = Query(None)):
    image = get_next_image(last_image_id)

    if not image:
        raise HTTPException(status_code=404, detail="No more images found")

    return {"message": "Next image retrieved successfully", "data": image}


@router.get("/api/bomen_of_the_day")
async def bomen_of_the_day():
    bomen_data = get_bomen_of_the_day()
    if not bomen_data:
        raise HTTPException(status_code=404, detail="Bo-Men of the Day not found")

    return {"message": "Bo-Men of the Day retrieved successfully", "data": bomen_data}