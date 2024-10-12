import logging
from fastapi import FastAPI
# from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

# Load
app = FastAPI(docs_url="/documentation", redoc_url=None)
logger = logging.getLogger('uvicorn')

'''
Constants
'''
# AWS
# AWS_S3_ACCESS_KEY_ID = os.getenv('AWS_S3_ACCESS_KEY_ID')
# AWS_S3_SECRET_ACCESS_KEY = os.getenv('AWS_S3_SECRET_ACCESS_KEY')
# AWS_S3_PREDICTION_BUCKET_NAME = os.getenv('AWS_S3_PREDICTION_BUCKET_NAME')
# AWS_S3_MODEL_BUCKET_NAME = os.getenv('AWS_S3_MODEL_BUCKET_NAME')

UPLOADED_IMAGE_QUEUE = []


@app.put("/api/v1/queue_uploaded_image")
def queue_uploaded_image(image_name: str):
    if image_name in UPLOADED_IMAGE_QUEUE:
        return
    UPLOADED_IMAGE_QUEUE.append(image_name)
    return


def process_queue():
    # check if queue is empty and calls generate_image and generate_json
    return


def generate_image(image_name: str) -> bool:
    # attempts to generate image using OpenPose and returns true if successful.
    return False


def generate_json(image_name: str) -> bool:
    # attempts to generate json using OpenPose and returns true if successful.
    return False
