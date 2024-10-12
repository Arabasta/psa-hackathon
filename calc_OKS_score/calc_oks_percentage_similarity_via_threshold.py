import json
import math

def euclidean_distance(p1, p2):
    """Calculate the Euclidean distance between two points (x1, y1) and (x2, y2)"""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def get_keypoints_by_person_id(data, person_id):
    """Retrieve the keypoints for the given person_id from the data"""
    for person in data['people']:
        if person['person_id'][0] == person_id:
            keypoints = person['pose_keypoints_2d']
            return keypoints
    return None  # Return None if the person_id is not found

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
            distance = euclidean_distance(keypoints1[i], keypoints2[i])
            if distance <= threshold:
                matched_keypoints += 1
            total_keypoints += 1

    # Calculate percentage score
    if total_keypoints == 0:
        return 0  # If no valid keypoints, return 0
    return round((matched_keypoints / total_keypoints) * 100,2)

def compare_all_poses(json_file1, json_file2, threshold=10):
    """Compare all people between two JSON files, matching by person_id and using threshold-based matching"""
    with open(json_file1, 'r') as f1, open(json_file2, 'r') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

        for person1 in data1['people']:
            person_id = person1['person_id'][0]
            print(f"Comparing person_id {person_id}...")

            # Get keypoints for this person_id from both files
            keypoints1 = get_keypoints_by_person_id(data1, person_id)
            keypoints2 = get_keypoints_by_person_id(data2, person_id)

            if keypoints1 is None or keypoints2 is None:
                print(f"Person with ID {person_id} not found in both JSON files. Skipping...")
                continue

            # Normalize keypoints for comparison
            normalized_keypoints1 = normalize_keypoints(keypoints1)
            normalized_keypoints2 = normalize_keypoints(keypoints2)

            # Compare the poses using threshold-based matching
            similarity_score = threshold_based_matching(normalized_keypoints1, normalized_keypoints2, threshold)
            print(f"Pose similarity score for person_id {person_id}: {similarity_score}%")

# Example usage:
json_file1 = "20241012_084121_keypoints.json"  # Replace with your file path
json_file2 = "20241012_084121_bgRemoved_keypoints.json"  # Replace with your file path
threshold = 10  # Set the threshold for matching (in pixels)
compare_all_poses(json_file1, json_file2, threshold)
