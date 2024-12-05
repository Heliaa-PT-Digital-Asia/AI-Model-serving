import numpy as np

def calculate_hip_rotation_internal_angle(keypoints, frame_shape, rotation_type, side):
    y, x = frame_shape[0], frame_shape[1]

    # Select the correct keypoints for left or right hip, knee, and ankle
    if side == 'left':
        hip_index, knee_index, ankle_index = 11, 13, 15
    else:
        hip_index, knee_index, ankle_index = 12, 14, 16

    # Get coordinates of the hip, knee, and ankle
    hip = np.array([keypoints[hip_index]['x'] * x, keypoints[hip_index]['y'] * y])
    knee = np.array([keypoints[knee_index]['x'] * x, keypoints[knee_index]['y'] * y])
    ankle = np.array([keypoints[ankle_index]['x'] * x, keypoints[ankle_index]['y'] * y])

    # Calculate vectors
    upper_leg_vector = knee - hip
    lower_leg_vector = ankle - knee

    # For internal rotation, calculate the angle when the leg moves toward the body
    if rotation_type == 'internal':
        reference_vector = np.array([1, 0])  # Horizontal reference
    else:
        reference_vector = np.array([-1, 0])  # Reverse for external rotation

    # Calculate angle between lower leg and the reference
    angle = np.degrees(np.arctan2(lower_leg_vector[1], lower_leg_vector[0]) - np.arctan2(reference_vector[1], reference_vector[0]))

    # Normalize the angle to be between 0 and 90 degrees
    if rotation_type == 'internal' and angle < 0:
        angle += 180

    rotation_angle = np.clip(angle, 0, 90)

    return rotation_angle

def calculate_hip_rotation_external_angle(keypoints, frame_shape, side):
    y, x = frame_shape[0], frame_shape[1]

    # Define indices for hip, knee, and ankle based on the side (left or right)
    if side == 'left':
        hip_index, knee_index, ankle_index = 11, 13, 15  # Left side keypoints
    else:
        hip_index, knee_index, ankle_index = 12, 14, 16  # Right side keypoints

    # Get coordinates of the hip, knee, and ankle
    hip = np.array([keypoints[hip_index]['x'] * x, keypoints[hip_index]['y'] * y])
    knee = np.array([keypoints[knee_index]['x'] * x, keypoints[knee_index]['y'] * y])
    ankle = np.array([keypoints[ankle_index]['x'] * x, keypoints[ankle_index]['y'] * y])

    # Vector for the thigh (hip to knee)
    thigh_vector = knee - hip

    # Vector for the lower leg (knee to ankle)
    lower_leg_vector = ankle - knee

    # Reference vector aligned with the body (assuming the leg is straight initially)
    reference_vector = np.array([0, 1])  # Vertical axis as the reference

    # Calculate the angle between the thigh vector and the reference vector
    angle = np.degrees(np.arctan2(thigh_vector[1], thigh_vector[0]) -
                       np.arctan2(reference_vector[1], reference_vector[0]))

    # Adjust angle based on the direction of the movement
    if angle < 0:
        angle += 360

    # Normalize angle for external rotation (adjusting for the correct direction)
    if side == 'left':
        angle = 360 - angle

    # Ensure the angle is within the range 0 to 90 degrees
    rotation_angle = np.clip(angle, 0, 90)

    return rotation_angle




def calculate_external_rotation_angle(keypoints, frame_shape, side):
    y, x = frame_shape[0], frame_shape[1]

    # Define indices for shoulder, elbow, and wrist based on the side (left or right)
    if side == 'left':
        shoulder_index, elbow_index, hand_index = 5, 7, 9  # Left side keypoints
    else:
        shoulder_index, elbow_index, hand_index = 6, 8, 10  # Right side keypoints

    # Get coordinates of the shoulder, elbow, and hand
    shoulder = np.array([keypoints[shoulder_index]['x'] * x, keypoints[shoulder_index]['y'] * y])
    elbow = np.array([keypoints[elbow_index]['x'] * x, keypoints[elbow_index]['y'] * y])
    hand = np.array([keypoints[hand_index]['x'] * x, keypoints[hand_index]['y'] * y])

    # Vector for the upper arm (shoulder to elbow)
    upper_arm_vector = elbow - shoulder

    # Vector for the forearm (elbow to hand)
    forearm_vector = hand - elbow

    # Project vectors onto the horizontal plane (ignore vertical movement)
    upper_arm_vector_horizontal = np.array([upper_arm_vector[0], 0])  # Horizontal movement of upper arm
    forearm_vector_horizontal = np.array([forearm_vector[0], forearm_vector[1]])  # Horizontal plane of forearm

    # Reference vector aligned with the body (starting forearm position across the body)
    reference_vector = np.array([-1, 0])  # Across the body as starting position for external rotation

    # Calculate the angle between the forearm and the reference vector
    angle = np.degrees(np.arctan2(forearm_vector_horizontal[1], forearm_vector_horizontal[0]) -
                       np.arctan2(reference_vector[1], reference_vector[0]))

    # Adjust angle for external rotation: as the forearm moves outward, the angle increases
    if angle < 0:
        angle += 180

    # For right side, reverse the calculation logic to ensure consistency
    if side == 'right':
        angle = 180 - angle

    # Ensure the angle is within the range 0 to 90 degrees, representing external rotation
    rotation_angle = np.clip(angle, 0, 90)

    return rotation_angle



def calculate_internal_rotation_angle(keypoints, frame_shape, side):
    y, x = frame_shape[0], frame_shape[1]

    # Define indices for shoulder, elbow, and wrist based on the side (left or right)
    if side == 'left':
        shoulder_index, elbow_index, hand_index = 5, 7, 9  # Left side keypoints
    else:
        shoulder_index, elbow_index, hand_index = 6, 8, 10  # Right side keypoints

    # Get coordinates of the shoulder, elbow, and hand
    shoulder = np.array([keypoints[shoulder_index]['x'] * x, keypoints[shoulder_index]['y'] * y])
    elbow = np.array([keypoints[elbow_index]['x'] * x, keypoints[elbow_index]['y'] * y])
    hand = np.array([keypoints[hand_index]['x'] * x, keypoints[hand_index]['y'] * y])

    # Vector for the upper arm (shoulder to elbow)
    upper_arm_vector = elbow - shoulder

    # Vector for the forearm (elbow to hand)
    forearm_vector = hand - elbow

    # Project vectors onto the horizontal plane (ignore vertical movement)
    upper_arm_vector_horizontal = np.array([upper_arm_vector[0], 0])  # Horizontal movement of upper arm
    forearm_vector_horizontal = np.array([forearm_vector[0], forearm_vector[1]])  # Horizontal plane of forearm

    # Reference vector aligned with the body (straight arm position)
    reference_vector = np.array([1, 0])  # Horizontal axis as the reference

    # Calculate the angle between the forearm and the reference vector
    angle = np.degrees(np.arctan2(forearm_vector_horizontal[1], forearm_vector_horizontal[0]) -
                       np.arctan2(reference_vector[1], reference_vector[0]))

    # Adjust angle based on the direction of the movement (ensure positive angles for internal rotation)
    if angle < 0:
        angle += 180

    # Normalize angle calculation for right side (reverse the calculation for consistency)
    if side == 'right':
        angle = 180 - angle

    # Ensure the angle is within the range 0 to 90 degrees, representing internal rotation
    rotation_angle = np.clip(angle, 0, 90)

    return rotation_angle




def calculate_shoulder_vertical_extension(keypoints, frame_shape, side):
    y, x = frame_shape[0], frame_shape[1]
    if side == 'left':
        shoulder_index, elbow_index = 5, 7  # Left shoulder and left elbow
    else:
        shoulder_index, elbow_index = 6, 8  # Right shoulder and right elbow for right side

    shoulder = np.array([keypoints[shoulder_index]['x'] * x, keypoints[shoulder_index]['y'] * y])
    elbow = np.array([keypoints[elbow_index]['x'] * x, keypoints[elbow_index]['y'] * y])

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


def calculate_neck_extension_angle(keypoints, frame_shape):
    y, x = frame_shape[0], frame_shape[1]

    # Nose or chin keypoint (depending on the model's output)
    nose_x = keypoints[0]['x'] * x
    nose_y = keypoints[0]['y'] * y

    # Shoulders (left and right)
    left_shoulder_x = keypoints[5]['x'] * x
    left_shoulder_y = keypoints[5]['y'] * y
    right_shoulder_x = keypoints[6]['x'] * x
    right_shoulder_y = keypoints[6]['y'] * y

    # Midpoint of shoulders
    shoulder_midpoint_x = (left_shoulder_x + right_shoulder_x) / 2
    shoulder_midpoint_y = (left_shoulder_y + right_shoulder_y) / 2

    # Vector from shoulder midpoint to nose (neck vector)
    neck_vector = np.array([nose_x - shoulder_midpoint_x, nose_y - shoulder_midpoint_y])

    # Vertical reference vector (pointing straight up)
    vertical_vector = np.array([0, -1])  # This points straight up (negative y-direction in image coordinates)

    # Calculate the angle between the neck vector and the vertical vector
    dot_product = np.dot(neck_vector, vertical_vector)
    neck_magnitude = np.linalg.norm(neck_vector) * np.linalg.norm(vertical_vector)
    
    # Avoid division by zero
    if neck_magnitude == 0:
        return 0

    # Calculate angle in degrees
    angle = np.degrees(np.arccos(dot_product / neck_magnitude))

    # Return the calculated angle for neck extension (adjusted for the vertical axis)
    return angle


def calculate_neck_flexion_angle(keypoints, frame_shape):
    y, x = frame_shape[0], frame_shape[1]

    # Nose or chin keypoint (depending on the model's output)
    nose_x = keypoints[0]['x'] * x
    nose_y = keypoints[0]['y'] * y

    # Shoulders (left and right)
    left_shoulder_x = keypoints[5]['x'] * x
    left_shoulder_y = keypoints[5]['y'] * y
    right_shoulder_x = keypoints[6]['x'] * x
    right_shoulder_y = keypoints[6]['y'] * y

    # Midpoint of shoulders
    shoulder_midpoint_x = (left_shoulder_x + right_shoulder_x) / 2
    shoulder_midpoint_y = (left_shoulder_y + right_shoulder_y) / 2

    # Vector from shoulder midpoint to nose (neck vector)
    neck_vector = np.array([nose_x - shoulder_midpoint_x, nose_y - shoulder_midpoint_y])

    # Vertical reference vector (pointing straight up)
    vertical_vector = np.array([0, -1])  # This points straight up (negative y-direction in image coordinates)

    # Calculate the angle between the neck vector and the vertical vector
    dot_product = np.dot(neck_vector, vertical_vector)
    neck_magnitude = np.linalg.norm(neck_vector) * np.linalg.norm(vertical_vector)
    
    # Avoid division by zero
    if neck_magnitude == 0:
        return 0

    # Calculate angle in degrees
    angle = np.degrees(np.arccos(dot_product / neck_magnitude))

    # Return the calculated angle for neck flexion (adjusted for the vertical axis)
    return angle
    

    
def calculate_neck_tilt(keypoints, frame_shape, side):
    """
    Calculate the neck tilt angle for left or right side tilt using head (nose) and shoulders.
    """
    y, x = frame_shape[0], frame_shape[1]
    nose = np.array([keypoints[0]['x'] * x, keypoints[0]['y'] * y])  # Nose (head) position
    left_shoulder = np.array([keypoints[5]['x'] * x, keypoints[5]['y'] * y])
    right_shoulder = np.array([keypoints[6]['x'] * x, keypoints[6]['y'] * y])
    
    # Calculate midpoint for neck (between shoulders)
    shoulder_midpoint = (left_shoulder + right_shoulder) / 2
    
    # Reference point for vertical (directly above the shoulder midpoint)
    vertical_ref = np.array([shoulder_midpoint[0], shoulder_midpoint[1] - 100])  # Adjust for better scaling
    
    # Vector from shoulder midpoint to vertical reference (ideal vertical position)
    vertical_vector = vertical_ref - shoulder_midpoint
    
    # Vector from the nose (head) to the shoulder midpoint
    head_vector = nose - shoulder_midpoint
    
    # Calculate the angle between the head vector and the vertical vector
    dot_product = np.dot(head_vector, vertical_vector)
    magnitude = np.linalg.norm(head_vector) * np.linalg.norm(vertical_vector)
    angle = np.degrees(np.arccos(dot_product / magnitude))
    
    # Adjust based on the side of the tilt (ignore angles when moving in the wrong direction)
    if side == 'right':
        # Only calculate angle if the nose is to the left of the shoulder midpoint (head tilted left)
        if nose[0] > shoulder_midpoint[0]:
            angle = 0  # Head is moving towards the right, no left tilt
    elif side == 'left':
        # Only calculate angle if the nose is to the right of the shoulder midpoint (head tilted right)
        if nose[0] < shoulder_midpoint[0]:
            angle = 0  # Head is moving towards the left, no right tilt
    
    return angle



def calculate_lateral_flexion_angle(keypoints, frame_shape):
    """
    Calculate the lateral flexion angle for both the left and right sides by measuring the angle relative to the horizontal axis.
    """
    y, x = frame_shape[0], frame_shape[1]
    # Get the keypoints for shoulders and hips
    left_shoulder = np.array([keypoints[5]['x'] * x, keypoints[5]['y'] * y])
    left_hip = np.array([keypoints[11]['x'] * x, keypoints[11]['y'] * y])
    right_shoulder = np.array([keypoints[6]['x'] * x, keypoints[6]['y'] * y])
    right_hip = np.array([keypoints[12]['x'] * x, keypoints[12]['y'] * y])

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
    y, x = frame_shape[0], frame_shape[1]
    angles = []

    # Assume vertical up is (0, -1) because the y-coordinate increases downwards in image coordinates
    vertical_up = np.array([0, -1])

    for shoulder_index, elbow_index in [(5, 7), (6, 8)]:  # Left and right arms
        shoulder = np.array([keypoints[shoulder_index]['x'] * x, keypoints[shoulder_index]['y'] * y])
        elbow = np.array([keypoints[elbow_index]['x'] * x, keypoints[elbow_index]['y'] * y])

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
    y, x = frame_shape[0], frame_shape[1]
    hip_index = 11 if side == 'left' else 12  # Left hip (11) or right hip (12)
    knee_index = 13 if side == 'left' else 14  # Left knee (13) or right knee (14)

    hip = np.array([keypoints[hip_index]['x'] * x, keypoints[hip_index]['y'] * y])
    knee = np.array([keypoints[knee_index]['x'] * x, keypoints[knee_index]['y'] * y])

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
    y, x = frame_shape[0], frame_shape[1]
    if side == 'left':
        shoulder_index, elbow_index = 5, 7  # Left shoulder and elbow
    else:
        shoulder_index, elbow_index = 6, 8  # Right shoulder and elbow

    shoulder = np.array([keypoints[shoulder_index]['x'] * x, keypoints[shoulder_index]['y'] * y])
    elbow = np.array([keypoints[elbow_index]['x'] * x, keypoints[elbow_index]['y'] * y])

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



def calculate_back_flexion_angle(keypoints, frame_shape):
    """Calculate the back flexion angle based on shoulders and hips."""
    y, x = frame_shape[0], frame_shape[1]
    left_shoulder = np.array([keypoints[5]['x'] * x, keypoints[5]['y'] * y])
    right_shoulder = np.array([keypoints[6]['x'] * x, keypoints[6]['y'] * y])
    left_hip = np.array([keypoints[11]['x'] * x, keypoints[11]['y'] * y])
    right_hip = np.array([keypoints[12]['x'] * x, keypoints[12]['y'] * y])

    shoulder_midpoint = (left_shoulder + right_shoulder) / 2
    hip_midpoint = (left_hip + right_hip) / 2

    spine_vector = hip_midpoint - shoulder_midpoint
    vertical_vector = np.array([0, 1])  # Vertical up

    dot_product = np.dot(spine_vector, vertical_vector)
    magnitude = np.linalg.norm(spine_vector) * np.linalg.norm(vertical_vector)
    cosine_angle = dot_product / magnitude
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)


def determine_risk(angle, risk_ranges):
    """Determine risk level based on angle."""
    if risk_ranges['low'][0] <= angle <= risk_ranges['low'][1]:
        return 'Low Risk'
    elif risk_ranges['medium'][0] <= angle < risk_ranges['medium'][1]:
        return 'Medium Risk'
    else:
        return 'High Risk'
