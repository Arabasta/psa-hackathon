import os
import logging
import random
from pathlib import Path

from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

# Initialise FastAPI and logger
app = FastAPI(docs_url="/documentation", redoc_url=None)
logger = logging.getLogger('uvicorn')

# Constants
CURRENT_BOMEN_NAME = ""
RAW_IMAGE_DIR = str(Path(__file__).parent)+"/raw_image"
RENDERED_IMAGE_DIR = str(Path(__file__).parent)+"/rendered_image"  # todo: remove dummy images
JSON_DIR = str(Path(__file__).parent)+"/json"


# Note: before calling this api, ensure that the raw images are already saved into RAW_IMAGE_DIR
@app.put("/api/v1/process_raw_image_from_dir")
def process_raw_image_from_dir(image_name: str) -> bool:
    try:
        raw_image_names = Utils.get_files_with_paths(RAW_IMAGE_DIR, ".png")
        if image_name not in raw_image_names:
            raise Exception(image_name+" not in "+RAW_IMAGE_DIR)

        if generate_image(image_name):
            generate_json(image_name)
            score = str(calculate_oks_score(image_name, CURRENT_BOMEN_NAME))
            # append score to image_name. e.g., x/12345_image_name.png -> x/12345_image_name_99.png
            os.rename(image_name+'.png', image_name+'_'+score+'.png')
            return True
        else:
            raise Exception(image_name+" keypoint generation failed ")

    except Exception as e:
        return False


def generate_image(image_name: str) -> bool:
    # attempts to generate image using OpenPose
    # if successful, store image at RENDERED_IMAGE_DIR
    #       return true
    return False


def generate_json(image_name: str) -> bool:
    # attempts to generate json using OpenPose
    # if successful, store json at JSON_DIR
    #       return true
    return False


def calculate_oks_score(image_name, current_bomen_name) -> float:
    # retrieve json of image_name and current_bomen_name from JSON_DIR
    # perform calculation
    return -1


def change_current_bomen():
    global CURRENT_BOMEN_NAME
    logger.info(CURRENT_BOMEN_NAME)
    all_rendered_image_names = Utils.get_files_with_paths(RENDERED_IMAGE_DIR, ".png")
    other_rendered_image_names = [x for x in all_rendered_image_names if x != CURRENT_BOMEN_NAME]
    CURRENT_BOMEN_NAME = random.choice(other_rendered_image_names)
    return


@app.on_event("startup")
def startup_event():
    scheduler = BackgroundScheduler(logger=logger)
    # scheduler to rotate Bo-Men image every X minutes/hours
    scheduler.add_job(change_current_bomen, 'interval', seconds=1)  # todo: change interval to 1 'minutes' during demo.
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


class Utils:
    @staticmethod
    def get_files_with_paths(directory, file_extension) -> [str]:
        file_paths = {}
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(f"{file_extension}"):  # e.g. '.pkl' files
                    full_path = os.path.join(root, file)
                    file_paths[file] = full_path
        return file_paths
