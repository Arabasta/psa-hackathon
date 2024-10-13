from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Query
from services import (upload_image_to_storage, store_submission_in_firestore, get_submission_from_firestore,
                      get_random_image, get_next_images)
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
    image_url = await upload_image_to_storage(image)

    # store metadata in Firestore
    submission_data = store_submission_in_firestore(image_url, image_caption, employees)

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


@router.get("/api/next_images")
async def next_images(last_image_id: str = Query(None), limit: int = 5):
    images = get_next_images(last_image_id, limit)

    if not images:
        raise HTTPException(status_code=404, detail="No more images found")

    return {"message": "Next images retrieved successfully", "data": images}