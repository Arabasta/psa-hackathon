import os
import logging
import random
import subprocess, sys
from pathlib import Path

from fastapi import FastAPI
from routes import router
from apscheduler.schedulers.background import BackgroundScheduler

from routes import random_image

# Initialise FastAPI and logger
app = FastAPI(docs_url="/documentation", redoc_url=None)
app.include_router(router)
logger = logging.getLogger('uvicorn')

# Constants
CURRENT_BOMEN_NAME = ""
RAW_IMAGE_DIR = str(Path(__file__).parent)+"/raw_image"
RENDERED_IMAGE_DIR = str(Path(__file__).parent)+"/rendered_image"
JSON_DIR = str(Path(__file__).parent)+"/json"


# Note: before calling this api, ensure that the raw images are already saved into RAW_IMAGE_DIR
@app.put("/api/v1/process_raw_image_from_dir")
def process_raw_image_from_dir(image_name: str) -> bool:
    try:
        logger.info("Initiate Processing: "+image_name)
        raw_image_names = Utils.get_files(RAW_IMAGE_DIR, ".jpg")
        if image_name+".jpg" not in raw_image_names:
            logger.warn(image_name+".jpg not in RAW_IMAGE_DIR")
            raise Exception(image_name+" not in "+RAW_IMAGE_DIR)

        if generate_image(image_name) and generate_json(image_name):
            score = str(calculate_oks_score(image_name, CURRENT_BOMEN_NAME))
            # append score to image_name. e.g., x/12345_image_name.png -> x/12345_image_name_99.png
            os.rename(image_name+'.png', image_name+'_'+score+'.png')
            logger.info("generate_image and generate_json success")
            return True
        else:
            logger.warn(image_name+" keypoint generation failed")
            raise Exception(image_name+" keypoint generation failed")

    except Exception as e:
        return False


def generate_image(image_name: str) -> bool:
    logger.info("-- Generating image ... generate_image(): "+image_name)
    all_rendered_image_names = Utils.get_files(RENDERED_IMAGE_DIR, ".png")
    if image_name+'_rendered.png' in all_rendered_image_names:
        logger.info(image_name+" was already generated. skipping generate_image().")
        return True
    global RAW_IMAGE_DIR
    # get powershell path - ref: https://stackoverflow.com/a/76404949
    process = subprocess.Popen("where powershell", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout, stderr = stdout.decode('utf-8'), stderr.decode('utf-8')
    powershell_path = stdout.strip()
    # generate image using ps1 script. if successful, store json at JSON_DIR and return true
    image_script_path = f"C:\\Users\Heaty\source\\repos\\psa-hackathon\\openpose\\wrapper_script_image.ps1"
    parent_path = Path(image_script_path).parent
    p = subprocess.Popen([powershell_path, '-c', 'Set-Location \"{}\";'.format(parent_path), image_script_path], stdout=sys.stdout)
    p.communicate()
    all_rendered_image_names = Utils.get_files(RENDERED_IMAGE_DIR, ".png")
    if image_name+'_rendered.png' in all_rendered_image_names:
        return True
    logger.info(image_name+'_rendered.png')
    logger.info(all_rendered_image_names)
    return False


def generate_json(image_name: str) -> bool:
    logger.info("-- Generating keypoints.json ... generate_json(): "+image_name)
    all_json_names = Utils.get_files(JSON_DIR, ".json")
    if image_name+'_keypoints.json' in all_json_names:
        logger.info(image_name+" was already generated. skipping generate_json().")
        return True
    global RAW_IMAGE_DIR
    # get powershell path - ref: https://stackoverflow.com/a/76404949
    process = subprocess.Popen("where powershell", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout, stderr = stdout.decode('utf-8'), stderr.decode('utf-8')
    powershell_path = stdout.strip()
    # generate json using ps1 script. if successful, store json at JSON_DIR and return true
    json_script_path = f"C:\\Users\Heaty\source\\repos\\psa-hackathon\\openpose\\wrapper_script_json.ps1"
    parent_path = Path(json_script_path).parent
    p = subprocess.Popen([powershell_path, '-c', 'Set-Location \"{}\";'.format(parent_path), json_script_path], stdout=sys.stdout)
    p.communicate()
    all_json_names = Utils.get_files(JSON_DIR, ".json")
    if image_name+'_keypoints.json' in all_json_names:
        return True
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
        logger.info("Initialise FastAPI Backend")
        logger.info(random_image)
        logger.info("end")
        # scheduler.start()
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

    @staticmethod
    def get_files(directory, file_extension) -> [str]:
        file_names = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(f"{file_extension}"):  # e.g. '.pkl' files
                    full_path = os.path.join(root, file)
                    file_names.append(file)
        return file_names
