import numpy as np

def calculate_spine_angle(keypoints, frame_shape, exercise_type):
    y, x = frame_shape[0], frame_shape[1]
    left_shoulder = np.array([keypoints[5]['x'] * x, keypoints[5]['y'] * y])
    right_shoulder = np.array([keypoints[6]['x'] * x, keypoints[6]['y'] * y])
    left_hip = np.array([keypoints[11]['x'] * x, keypoints[11]['y'] * y])
    right_hip = np.array([keypoints[12]['x'] * x, keypoints[12]['y'] * y])

    shoulder_midpoint = (left_shoulder + right_shoulder) / 2
    hip_midpoint = (left_hip + right_hip) / 2

    if exercise_type in ['flexion', 'extension']:
        reference_line = hip_midpoint - shoulder_midpoint if exercise_type == 'flexion' else shoulder_midpoint - hip_midpoint
    elif exercise_type == 'lateral':
        reference_line = right_shoulder - left_shoulder

    vertical_line = np.array([0, 1]) * np.linalg.norm(reference_line)
    dot_product = np.dot(reference_line, vertical_line)
    magnitude = np.linalg.norm(reference_line) * np.linalg.norm(vertical_line)
    angle = np.degrees(np.arccos(dot_product / magnitude))

    return angle if exercise_type != 'extension' else 180 - angle

def calculate_lateral_flexion_angle(keypoints, frame_shape):
    y, x = frame_shape
    left_shoulder = np.array([keypoints[5]['x'] * x, keypoints[5]['y'] * y])
    left_hip = np.array([keypoints[11]['x'] * x, keypoints[11]['y'] * y])
    right_shoulder = np.array([keypoints[6]['x'] * x, keypoints[6]['y'] * y])
    right_hip = np.array([keypoints[12]['x'] * x, keypoints[12]['y'] * y])

    left_vector = left_shoulder - left_hip
    right_vector = right_shoulder - right_hip

    left_angle = np.degrees(np.arctan2(left_vector[1], left_vector[0]))
    right_angle = np.degrees(np.arctan2(right_vector[1], right_vector[0]))

    left_angle = 90 - np.abs(left_angle)
    right_angle = 90 - np.abs(right_angle)

    return max(left_angle, right_angle)

def calculate_knee_raise_angle(keypoints, frame_shape, side):
    y, x = frame_shape
    hip_index = 11 if side == 'left' else 12
    knee_index = 13 if side == 'left' else 14

    hip = np.array([keypoints[hip_index]['x'] * x, keypoints[hip_index]['y'] * y])
    knee = np.array([keypoints[knee_index]['x'] * x, keypoints[knee_index]['y'] * y])

    vertical_ref = np.array([hip[0], hip[1] + 100])
    knee_vector = knee - hip
    vertical_vector = vertical_ref - hip

    dot_product = np.dot(knee_vector, vertical_vector)
    magnitude = np.linalg.norm(knee_vector) * np.linalg.norm(vertical_vector)
    angle = np.degrees(np.arccos(dot_product / magnitude))

    return angle

def calculate_vertical_flexion_angle(keypoints, frame_shape, side):
    y, x = frame_shape
    shoulder_index, elbow_index = (5, 7) if side == 'left' else (6, 8)

    shoulder = np.array([keypoints[shoulder_index]['x'] * x, keypoints[shoulder_index]['y'] * y])
    elbow = np.array([keypoints[elbow_index]['x'] * x, keypoints[elbow_index]['y'] * y])

    arm_vector = elbow - shoulder
    vertical_up = np.array([0, 1])

    dot_product = np.dot(arm_vector / np.linalg.norm(arm_vector), vertical_up)
    angle = np.degrees(np.arccos(dot_product))

    return angle

def calculate_abduction_angle(keypoints, frame_shape):
    y, x = frame_shape
    shoulder_index, elbow_index = (5, 7), (6, 8)

    angles = []
    vertical_up = np.array([0, -1])

    for s_idx, e_idx in shoulder_index:
        shoulder = np.array([keypoints[s_idx]['x'] * x, keypoints[s_idx]['y'] * y])
        elbow = np.array([keypoints[e_idx]['x'] * x, keypoints[e_idx]['y'] * y])

        arm_vector = elbow - shoulder
        dot_product = np.dot(arm_vector / np.linalg.norm(arm_vector), vertical_up)
        angle = np.degrees(np.arccos(dot_product))
        corrected_angle = 180 - angle
        angles.append(corrected_angle)

    return min(angles)

def determine_risk(angle, risk_ranges):
    """Determine risk level based on angle."""
    if risk_ranges['low'][0] <= angle <= risk_ranges['low'][1]:
        return 'Low Risk'
    elif risk_ranges['medium'][0] <= angle < risk_ranges['medium'][1]:
        return 'Medium Risk'
    else:
        return 'High Risk'
