from flask import Flask, request, jsonify
import json
import numpy as np
import pandas as pd

app = Flask(__name__)


# Configuration dictionary for exercises
exercise_config = {
    'back_flexion': {
        'keypoints': [5, 6, 11, 12],
        'angle_function': lambda kp, shape: calculate_spine_angle(kp, shape, 'flexion'),
        'angle_max':90,
        'movement_threshold': 20,
        'risk_ranges': {'low': (60, 90), 'medium': (31, 59), 'high': (0, 30)}
    },
    'back_extension': {
        'keypoints': [5, 6, 11, 12],
        'angle_function': lambda kp, shape: calculate_spine_angle(kp, shape, 'extension'),
        'angle_max':30,
        'movement_threshold': 10,
        'risk_ranges': {'low': (21, 30), 'medium': (11, 20), 'high': (0, 10)}
    },
    'lateral_flexion': {
        'keypoints': [5, 6, 11, 12],  # Both shoulders and both hips
        'angle_function': lambda kp, shape: calculate_lateral_flexion_angle(kp, shape),
        'angle_max': 45,
        'movement_threshold': 10,
        'risk_ranges': {'low': (27, 45), 'medium': (15, 26), 'high': (0, 14)}
    },
    'knee_raise_left': {
        'keypoints': [11, 13],  # Left hip and left knee
        'angle_function': lambda kp, shape: calculate_knee_raise_angle(kp, shape, 'left'),
        'angle_max': 120,
        'movement_threshold': 15,
        'risk_ranges': {'low': (91, 120), 'medium': (50, 90), 'high': (0, 49)}
    },
    'knee_raise_right': {
        'keypoints': [12, 14],  # Right hip and right knee
        'angle_function': lambda kp, shape: calculate_knee_raise_angle(kp, shape, 'right'),
        'angle_max': 120,
        'movement_threshold': 15,
        'risk_ranges': {'low': (91, 120), 'medium': (50, 90), 'high': (0, 49)}
    },
    'right_shoulder_vertical_flexion': {
        'keypoints': [6, 8],  # Right shoulder and right elbow
        'angle_function': lambda kp, shape: calculate_vertical_flexion_angle(kp, shape, 'right'),
        'angle_max': 180,
        'movement_threshold': 30,
        'risk_ranges': {'low': (120, 180), 'medium': (51, 119), 'high': (0, 50)}
    },
    'left_shoulder_vertical_flexion': {
        'keypoints': [5, 7],  # Left shoulder and left elbow
        'angle_function': lambda kp, shape: calculate_vertical_flexion_angle(kp, shape, 'left'),
        'angle_max': 180,
        'movement_threshold': 30,
        'risk_ranges': {'low': (120, 180), 'medium': (51, 119), 'high': (0, 50)}
    },
    'shoulder_abduction': {
        'keypoints': [5,6,8, 7],  
        'angle_function': lambda kp, shape: calculate_abduction_angle(kp, shape),
        'angle_max': 180,
        'movement_threshold': 30,
        'risk_ranges': {'low': (120, 180), 'medium': (51, 119), 'high': (0, 50)}
    }
}
def calculate_lateral_flexion_angle(keypoints, frame_shape):
    """
    Calculate the lateral flexion angle for both the left and right sides by measuring the angle relative to the horizontal axis.
    """
    y, x, _ = frame_shape
    # Get the keypoints for shoulders and hips
    left_shoulder = np.array([keypoints[5][x] * x, keypoints[5][y] * y])
    left_hip = np.array([keypoints[11][x] * x, keypoints[11][y] * y])
    right_shoulder = np.array([keypoints[6][x] * x, keypoints[6][y] * y])
    right_hip = np.array([keypoints[12][x] * x, keypoints[12][y] * y])

    # Calculate midpoints
    left_midpoint = (left_shoulder + left_hip) / 2
    right_midpoint = (right_shoulder + right_hip) / 2

    # Horizontal vector (constant)
    horizontal_vector = np.array([1, 0])

    # Calculate vectors from hip to shoulder for both sides
    left_vector = left_shoulder - left_hip
    right_vector = right_shoulder - right_hip

    # Calculate angles from horizontal
    left_angle = np.degrees(np.arctan2(left_vector[1], left_vector[0]))
    right_angle = np.degrees(np.arctan2(right_vector[1], right_vector[0]))

    # Correct angles to ensure they are measured from the horizontal
    left_angle = 90 - np.abs(left_angle)
    right_angle = 90 - np.abs(right_angle)

    # Return the maximum angle to account for both sides
    if left_angle > right_angle:
        
        return left_angle
    else:
        return right_angle



def calculate_abduction_angle(keypoints, frame_shape):
    y, x = frame_shape
    angles = []

    # Assume vertical up is (0, -1) because the y-coordinate increases downwards in image coordinates
    vertical_up = np.array([0, -1])

    for shoulder_index, elbow_index in [(5, 7), (6, 8)]:  # Left and right arms
        shoulder = np.array([keypoints[shoulder_index][x] * x, keypoints[shoulder_index][y] * y])
        elbow = np.array([keypoints[elbow_index][x] * x, keypoints[elbow_index][y] * y])

        # Calculate the arm vector
        arm_vector = elbow - shoulder
        arm_vector_normalized = arm_vector / np.linalg.norm(arm_vector)

        # Calculate the dot product and angle
        dot_product = np.dot(arm_vector_normalized, vertical_up)
        angle = np.degrees(np.arccos(dot_product))

        # Correct the angle so it starts from 0 when the arm is down
        corrected_angle = 180 - angle  # Reverse the angle measurement

        angles.append(corrected_angle)

    # Return the minimum angle from either side
    return min(angles)  # Use min to reflect the smallest angle (most raised position)




def calculate_knee_raise_angle(keypoints, frame_shape, side):
    """Calculate the knee raise angle for the specified side."""
    y, x, _ = frame_shape
    hip_index = 11 if side == 'left' else 12  # Left hip (11) or right hip (12)
    knee_index = 13 if side == 'left' else 14  # Left knee (13) or right knee (14)

    hip = np.array([keypoints[hip_index][x] * x, keypoints[hip_index][y] * y])
    knee = np.array([keypoints[knee_index][x] * x, keypoints[knee_index][y] * y])

    # Create a vertical reference point directly below the hip for a vertical line comparison
    vertical_ref = np.array([hip[0], hip[1] + 100])  # +100 to create a point directly below

    # Vector from hip to knee, and from hip to vertical reference
    knee_vector = knee - hip
    vertical_vector = vertical_ref - hip

    # Calculate angle from vertical
    dot_product = np.dot(knee_vector, vertical_vector)
    magnitude = np.linalg.norm(knee_vector) * np.linalg.norm(vertical_vector)
    angle = np.degrees(np.arccos(dot_product / magnitude))

    return angle

# Calculate Vertical Flexion Angle Function
def calculate_vertical_flexion_angle(keypoints, frame_shape, side):
    y, x, _ = frame_shape
    if side == 'left':
        shoulder_index, elbow_index = 5, 7  # Left shoulder and elbow
    else:
        shoulder_index, elbow_index = 6, 8  # Right shoulder and elbow

    shoulder = np.array([keypoints[shoulder_index][x] * x, keypoints[shoulder_index][y] * y])
    elbow = np.array([keypoints[elbow_index][x] * x, keypoints[elbow_index][y] * y])

    # Calculate arm vector
    arm_vector = elbow - shoulder
    arm_vector_normalized = arm_vector / np.linalg.norm(arm_vector)

    # Define vertical up as (0, 1) since we are looking from the side
    vertical_up = np.array([0, 1])

    # Calculate the angle
    dot_product = np.dot(arm_vector_normalized, vertical_up)
    angle = np.degrees(np.arccos(dot_product))

    # Correct angle based on arm's position
    return angle
#     return 180 - angle if side == 'left' else angle  # Adjust depending on the side

# def calculate_spine_angle(keypoints, frame_shape, exercise_type):
#     """Calculate the spine angle for different types of exercises."""
#     y, x = frame_shape[0], frame_shape[1]
#     print ("alikarimi")
#     print (keypoints)
#     left_shoulder = np.array([keypoints[5][1] * x, keypoints[5][0] * y])
#     right_shoulder = np.array([keypoints[6][1] * x, keypoints[6][0] * y])
#     left_hip = np.array([keypoints[11][1] * x, keypoints[11][0] * y])
#     right_hip = np.array([keypoints[12][1] * x, keypoints[12][0] * y])

#     shoulder_midpoint = (left_shoulder + right_shoulder) / 2
#     hip_midpoint = (left_hip + right_hip) / 2

#     if exercise_type in ['flexion', 'extension']:
#         reference_line = hip_midpoint - shoulder_midpoint if exercise_type == 'flexion' else shoulder_midpoint - hip_midpoint
#     elif exercise_type == 'lateral':
#         # For lateral, we consider the line between the left and right shoulder
#         reference_line = right_shoulder - left_shoulder

#     vertical_line = np.array([0, 1]) * np.linalg.norm(reference_line)  # Vertical line
#     dot_product = np.dot(reference_line, vertical_line)
#     magnitude = np.linalg.norm(reference_line) * np.linalg.norm(vertical_line)
#     angle = np.degrees(np.arccos(dot_product / magnitude))

#     return angle if exercise_type != 'extension' else 180 - angle  # Adjust for 'extension'



def calculate_back_flexion_angle(keypoints, frame_shape):
    """Calculate the back flexion angle based on shoulders and hips."""
    y, x, _ = frame_shape  # Correctly unpack height, width, and channels
    left_shoulder = np.array([keypoints[5][x] * x, keypoints[5][y] * y])
    right_shoulder = np.array([keypoints[6][x] * x, keypoints[6][y] * y])
    left_hip = np.array([keypoints[11][x] * x, keypoints[11][y] * y])
    right_hip = np.array([keypoints[12][x] * x, keypoints[12][y] * y])

    shoulder_midpoint = (left_shoulder + right_shoulder) / 2
    hip_midpoint = (left_hip + right_hip) / 2

    spine_vector = hip_midpoint - shoulder_midpoint
    vertical_vector = np.array([0, 1])  # Vertical up

    dot_product = np.dot(spine_vector, vertical_vector)
    magnitude = np.linalg.norm(spine_vector) * np.linalg.norm(vertical_vector)
    cosine_angle = dot_product / magnitude
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)

def calculate_angle(keypoints, frame_shape, exercise_type):
    y, x, _ = frame_shape
    left_shoulder = np.array([keypoints[5][x] * x, keypoints[5][y] * y])
    right_shoulder = np.array([keypoints[6][x] * x, keypoints[6][y] * y])
    left_hip = np.array([keypoints[11][x] * x, keypoints[11][y] * y])
    right_hip = np.array([keypoints[12][x] * x, keypoints[12][y] * y])

    shoulder_midpoint = (left_shoulder + right_shoulder) / 2
    hip_midpoint = (left_hip + right_hip) / 2

    spine_vector = hip_midpoint - shoulder_midpoint
    vertical_vector = np.array([0, 1])  # Assuming vertical up

    dot_product = np.dot(spine_vector, vertical_vector)
    magnitude = np.linalg.norm(spine_vector) * np.linalg.norm(vertical_vector)
    cosine_angle = dot_product / magnitude
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    print("typesh")
    print( exercise_type)
    return np.degrees(angle)

def calculate_spine_angle(keypoints, frame_shape, exercise_type):
    y, x = frame_shape[0], frame_shape[1]
    print (keypoints)

    left_shoulder = np.array([keypoints[5]['x'] * x, keypoints[5]['y'] * y])
    right_shoulder = np.array([keypoints[6]['x'] * x, keypoints[6]['y'] * y])
    left_hip = np.array([keypoints[11]['x'] * x, keypoints[11]['y'] * y])
    right_hip = np.array([keypoints[12]['x'] * x, keypoints[12]['y'] * y])

    shoulder_midpoint = (left_shoulder + right_shoulder) / 2
    hip_midpoint = (left_hip + right_hip) / 2

    if exercise_type in ['flexion', 'extension']:
        reference_line = hip_midpoint - shoulder_midpoint if exercise_type == 'flexion' else shoulder_midpoint - hip_midpoint
    elif exercise_type == 'lateral':
        # For lateral, we consider the line between the left and right shoulder
        reference_line = right_shoulder - left_shoulder

    vertical_line = np.array([0, 1]) * np.linalg.norm(reference_line)  # Vertical line
    dot_product = np.dot(reference_line, vertical_line)
    magnitude = np.linalg.norm(reference_line) * np.linalg.norm(vertical_line)
    angle = np.degrees(np.arccos(dot_product / magnitude))

    return angle if exercise_type != 'extension' else 180 - angle  # Adjust for 'extension'


def determine_risk(angle, risk_ranges):
    """Determine risk level based on angle."""
    if risk_ranges['low'][0] <= angle <= risk_ranges['low'][1]:
        return 'Low Risk'
    elif risk_ranges['medium'][0] <= angle < risk_ranges['medium'][1]:
        return 'Medium Risk'
    else:
        return 'High Risk'

@app.route('/calculate-angle', methods=['POST'])
def calculate_angle():
    data = request.json
    if 'meta' not in data or 'content' not in data:
        return jsonify({"error": "Invalid JSON structure"}), 400

    frame_shape = (data['meta']['frame_shape']['y'], data['meta']['frame_shape']['x'])
    keypoints_data = data['content']
    exercise_type = data['meta']['exercise_type']  
    angles_data = []
    config = exercise_config[exercise_type]

    for frame in keypoints_data:
        keypoints = frame['data']
        if len(keypoints) > 0 :
            dict_keypoints ={kp['id']: kp for kp in keypoints}
            if len(dict_keypoints.keys()) == len(config['keypoints']):
                angle = config['angle_function'](dict_keypoints, frame_shape)
        else :
            angle = 0 
        
        if 0 < angle < config['angle_max']: # Ensure the angle is within a valid range
            angles_data.append({
                'Time': frame['time'],
                'Angle': angle
            })

    # Select the top 12 highest angles
    df = pd.DataFrame(angles_data)
    if not df.empty:
        df = df.nlargest(12, 'Angle')
        print(df)
        average_angle = df['Angle'].mean()

    # if angles_data:
        # average_angle = np.mean(angles_data)
        risk_label = determine_risk(average_angle, config['risk_ranges'])
        response = {
            "average_angle": average_angle,
            "risk_label": risk_label
        }
    else:
        response = {
            "error": "No valid angles found"
        }

    return jsonify(response)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
