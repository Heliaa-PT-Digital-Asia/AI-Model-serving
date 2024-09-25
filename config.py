from angle_functions import calculate_spine_angle, calculate_lateral_flexion_angle, calculate_knee_raise_angle, calculate_vertical_flexion_angle, calculate_abduction_angle

# Configuration dictionary for exercises
exercise_config = {
    'back_flexion': {
        'keypoints': [5, 6, 11, 12],
        'angle_function': lambda kp, shape: calculate_spine_angle(kp, shape, 'flexion'),
        'angle_max': 90,
        'movement_threshold': 20,
        'risk_ranges': {'low': (60, 90), 'medium': (31, 59), 'high': (0, 30)}
    },
    'back_extension': {
        'keypoints': [5, 6, 11, 12],
        'angle_function': lambda kp, shape: calculate_spine_angle(kp, shape, 'extension'),
        'angle_max': 30,
        'movement_threshold': 10,
        'risk_ranges': {'low': (21, 30), 'medium': (11, 20), 'high': (0, 10)}
    },
    'lateral_flexion': {
        'keypoints': [5, 6, 11, 12],
        'angle_function': lambda kp, shape: calculate_lateral_flexion_angle(kp, shape),
        'angle_max': 45,
        'movement_threshold': 10,
        'risk_ranges': {'low': (27, 45), 'medium': (15, 26), 'high': (0, 14)}
    },
    'knee_raise_left': {
        'keypoints': [11, 13],
        'angle_function': lambda kp, shape: calculate_knee_raise_angle(kp, shape, 'left'),
        'angle_max': 120,
        'movement_threshold': 15,
        'risk_ranges': {'low': (91, 120), 'medium': (50, 90), 'high': (0, 49)}
    },
    'knee_raise_right': {
        'keypoints': [12, 14],
        'angle_function': lambda kp, shape: calculate_knee_raise_angle(kp, shape, 'right'),
        'angle_max': 120,
        'movement_threshold': 15,
        'risk_ranges': {'low': (91, 120), 'medium': (50, 90), 'high': (0, 49)}
    },
    'right_shoulder_vertical_flexion': {
        'keypoints': [6, 8],
        'angle_function': lambda kp, shape: calculate_vertical_flexion_angle(kp, shape, 'right'),
        'angle_max': 180,
        'movement_threshold': 30,
        'risk_ranges': {'low': (120, 180), 'medium': (51, 119), 'high': (0, 50)}
    },
    'left_shoulder_vertical_flexion': {
        'keypoints': [5, 7],
        'angle_function': lambda kp, shape: calculate_vertical_flexion_angle(kp, shape, 'left'),
        'angle_max': 180,
        'movement_threshold': 30,
        'risk_ranges': {'low': (120, 180), 'medium': (51, 119), 'high': (0, 50)}
    },
    'shoulder_abduction': {
        'keypoints': [5, 6, 8, 7],
        'angle_function': lambda kp, shape: calculate_abduction_angle(kp, shape),
        'angle_max': 180,
        'movement_threshold': 30,
        'risk_ranges': {'low': (120, 180), 'medium': (51, 119), 'high': (0, 50)}
    }
}
SECRET_KEY = "255621@G320dQq@#"  # Make this a strong secret key
