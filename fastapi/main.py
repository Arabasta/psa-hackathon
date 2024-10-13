import os
import logging
import random
import json
import math
import subprocess, sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from apscheduler.schedulers.background import BackgroundScheduler

from routes import random_image

# Initialise FastAPI and logger
app = FastAPI(docs_url="/documentation", redoc_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
        raw_image_names_png = Utils.get_files(RAW_IMAGE_DIR, ".png")
        raw_image_names.extend(raw_image_names_png)
        if image_name+".jpg" in raw_image_names or image_name+".png" in raw_image_names:
            pass
        else:
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
    image_name_path = Utils.get_keypoints_file_path(JSON_DIR, image_name, "json")
    current_bomen_name_path = Utils.get_keypoints_file_path(JSON_DIR, current_bomen_name, "json")
    return OKS.compare_all_poses(image_name_path, current_bomen_name_path)


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
        logger.info("start")
        process_raw_image_from_dir("20241012_084121_bgRemoved")
        calculate_oks_score("20241012_084121", "20241012_084121_bgRemoved")
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

    @staticmethod
    def get_keypoints_file_path(directory, file_name, file_extension) -> str:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(f"{file_name}_keypoints.{file_extension}"):
                    return os.path.join(root, file)
        return ""


class OKS:
    @staticmethod
    def euclidean_distance(p1, p2):
        """Calculate the Euclidean distance between two points (x1, y1) and (x2, y2)"""
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    @staticmethod
    def get_keypoints_by_person_id(data, person_id):
        """Retrieve the keypoints for the given person_id from the data"""
        for person in data['people']:
            if person['person_id'][0] == person_id:
                keypoints = person['pose_keypoints_2d']
                return keypoints
        return None  # Return None if the person_id is not found

    @staticmethod
    def normalize_keypoints(keypoints):
        """Normalize keypoints by centering and scaling them"""
        neck_x, neck_y = keypoints[3], keypoints[4]  # Use neck (index 1) as center
        normalized_keypoints = []
        for i in range(0, len(keypoints), 3):  # Step by 3: (x, y, confidence)
            if keypoints[i+2] > 0:  # If confidence is positive
                normalized_x = keypoints[i] - neck_x
                normalized_y = keypoints[i+1] - neck_y
                normalized_keypoints.append([normalized_x, normalized_y])
            else:
                normalized_keypoints.append([0, 0])  # Treat [0, 0, 0] as valid zero points
        return normalized_keypoints

    @staticmethod
    def threshold_based_matching(keypoints1, keypoints2, threshold=10):
        """
        Compare two sets of keypoints by checking how many are within a threshold distance.
        Returns the percentage of matched keypoints.
        """
        matched_keypoints = 0
        total_keypoints = 0

        # Iterate through keypoints and compare valid keypoints
        for i in range(len(keypoints1)):
            if keypoints1[i] == [0, 0] and keypoints2[i] == [0, 0]:
                # Both keypoints are [0, 0], consider this as a valid match
                continue  # No need to add to the count
            elif keypoints1[i] != [0, 0] and keypoints2[i] != [0, 0]:
                # Calculate Euclidean distance for valid keypoints
                distance = OKS.euclidean_distance(keypoints1[i], keypoints2[i])
                if distance <= threshold:
                    matched_keypoints += 1
                total_keypoints += 1

        # Calculate percentage score
        if total_keypoints == 0:
            return 0  # If no valid keypoints, return 0
        return round((matched_keypoints / total_keypoints) * 100,2)

    @staticmethod
    def compare_all_poses(json_file1, json_file2, threshold=10):
        """Compare all people between two JSON files, matching by person_id and using threshold-based matching"""
        with open(json_file1, 'r') as f1, open(json_file2, 'r') as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)

            for person1 in data1['people']:
                person_id = person1['person_id'][0]
                logger.info(f"Comparing person_id {person_id}...")

                # Get keypoints for this person_id from both files
                keypoints1 = OKS.get_keypoints_by_person_id(data1, person_id)
                keypoints2 = OKS.get_keypoints_by_person_id(data2, person_id)

                if keypoints1 is None or keypoints2 is None:
                    logger.info(f"Person with ID {person_id} not found in both JSON files. Skipping...")
                    continue

                # Normalize keypoints for comparison
                normalized_keypoints1 = OKS.normalize_keypoints(keypoints1)
                normalized_keypoints2 = OKS.normalize_keypoints(keypoints2)

                # Compare the poses using threshold-based matching
                similarity_score = OKS.threshold_based_matching(normalized_keypoints1, normalized_keypoints2, threshold)
                logger.info(f"Pose similarity score for person_id {person_id}: {similarity_score}%")

    # Example usage:
    json_file1 = "20241012_084121_keypoints.json"  # Replace with your file path
    json_file2 = "20241012_084121_bgRemoved_keypoints.json"  # Replace with your file path
    threshold = 10  # Set the threshold for matching (in pixels)
    # compare_all_poses(json_file1, json_file2, threshold)
