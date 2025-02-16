from angle_functions import calculate_spine_angle,calculate_external_rotation_angle, calculate_internal_rotation_angle, calculate_hip_rotation_internal_angle ,calculate_shoulder_vertical_extension ,calculate_neck_extension_angle ,calculate_lateral_flexion_angle, calculate_knee_raise_angle, calculate_vertical_flexion_angle, calculate_abduction_angle, calculate_torso_rotation_angle, calculate_hip_rotation_external_angle, calculate_neck_tilt, calculate_neck_flexion_angle

# Configuration dictionary for exercises
exercise_config = {
    'back_flexion': {
        'exercises_type':'back_flexion',
        'keypoints': [5, 6, 11, 12],
        'angle_function': lambda kp, shape: calculate_spine_angle(kp, shape, 'flexion'),
        'angle_max': 90,
        'angle_min' : 5,
        'movement_threshold': 20,
        'risk_ranges': {'low': (60, 90), 'medium': (31, 59), 'high': (0, 30)}
    },
    'back_extension': {
        'exercises_type':'back_extension',
        'keypoints': [5, 6, 11, 12],
        'angle_function': lambda kp, shape: calculate_spine_angle(kp, shape, 'extension'),
        'angle_max': 30,
        'angle_min' : 5,
        'movement_threshold': 10,
        'risk_ranges': {'low': (21, 30), 'medium': (11, 20), 'high': (0, 10)}
    },
    'lateral_flexion': {
        'exercises_type':'lateral_flexion',
        'keypoints': [5, 6, 11, 12],
        'angle_function': lambda kp, shape: calculate_lateral_flexion_angle(kp, shape),
        'angle_max': 45,
        'angle_min' : 5,
        'movement_threshold': 10,
        'risk_ranges': {'low': (27, 45), 'medium': (15, 26), 'high': (0, 14)}
    },
    'lateral_left_right_tilt': {
        'exercises_type':'lateral_left_right_tilt',
        'keypoints': [5, 6, 11, 12],
        'angle_function': lambda kp, shape: calculate_lateral_flexion_angle(kp, shape),
        'angle_max': 45,
        'angle_min' : 5,
        'movement_threshold': 10,
        'risk_ranges': {'low': (27, 45), 'medium': (15, 26), 'high': (0, 14)}
    },
    'knee_raise_left': {
        'exercises_type':'knee_raise_left',
        'keypoints': [11, 13],
        'angle_function': lambda kp, shape: calculate_knee_raise_angle(kp, shape, 'left'),
        'angle_max': 120,
        'angle_min' : 10,
        'movement_threshold': 15,
        'risk_ranges': {'low': (91, 120), 'medium': (50, 90), 'high': (0, 49)}
    },
    'knee_raise_right': {
        'exercises_type':'knee_raise_right',
        'keypoints': [12, 14],
        'angle_function': lambda kp, shape: calculate_knee_raise_angle(kp, shape, 'right'),
        'angle_max': 120,
        'angle_min' : 10,
        'movement_threshold': 15,
        'risk_ranges': {'low': (91, 120), 'medium': (50, 90), 'high': (0, 49)}
    },
    'right_shoulder_vertical_flexion': {
        'exercises_type':'right_shoulder_vertical_flexion',
        'keypoints': [6, 8],
        'angle_function': lambda kp, shape: calculate_vertical_flexion_angle(kp, shape, 'right'),
        'angle_max': 180,
        'angle_min' : 10,
        'movement_threshold': 30,
        'risk_ranges': {'low': (120, 180), 'medium': (51, 119), 'high': (0, 50)}
    },
    'left_shoulder_vertical_flexion': {
        'exercises_type':'left_shoulder_vertical_flexion',
        'keypoints': [5, 7],
        'angle_function': lambda kp, shape: calculate_vertical_flexion_angle(kp, shape, 'left'),
        'angle_max': 180,
        'angle_min': 10,
        'movement_threshold': 30,
        'risk_ranges': {'low': (120, 180), 'medium': (51, 119), 'high': (0, 50)}
    },
    'shoulder_vertical_flexion_right': {
        'exercises_type':'shoulder_vertical_flexion_right',
        'keypoints': [6, 8],
        'angle_function': lambda kp, shape: calculate_vertical_flexion_angle(kp, shape, 'right'),
        'angle_max': 180,
        'angle_min': 10,
        'movement_threshold': 30,
        'risk_ranges': {'low': (120, 180), 'medium': (51, 119), 'high': (0, 50)}
    },
    'shoulder_vertical_flexion_left': {
        'exercises_type':'shoulder_vertical_flexion_left',
        'keypoints': [5, 7],
        'angle_function': lambda kp, shape: calculate_vertical_flexion_angle(kp, shape, 'left'),
        'angle_max': 180,
        'angle_min': 10,
        'movement_threshold': 30,
        'risk_ranges': {'low': (120, 180), 'medium': (51, 119), 'high': (0, 50)}
    },
    'shoulder_abduction': {
        'exercises_type':'shoulder_abduction',
        'keypoints': [5, 6, 8, 7],
        'angle_function': lambda kp, shape: calculate_abduction_angle(kp, shape),
        'angle_max': 180,
        'angle_min': 10,
        'movement_threshold': 30,
        'risk_ranges': {'low': (120, 180), 'medium': (51, 119), 'high': (0, 50)}
    },
    'left_tilt': {
        'exercises_type':'left_tilt',
        'keypoints': [0, 5, 6],  # Nose, left shoulder, right shoulder
        'angle_function': lambda kp, shape: calculate_neck_tilt(kp, shape, 'left'),
        'angle_max': 45, 
        'angle_min': 5, # Maximum angle for neck tilt
        'movement_threshold': 5,
        'risk_ranges': {'low': (30, 45), 'medium': (15, 29), 'high': (0, 14)}
    },
    'right_tilt': {
        'exercises_type':'right_tilt',
        'keypoints': [0, 5, 6],  # Nose, left shoulder, right shoulder
        'angle_function': lambda kp, shape: calculate_neck_tilt(kp, shape, 'right'),
        'angle_max': 45,
        'angle_min': 5,  # Maximum angle for neck tilt
        'movement_threshold': 5,
        'risk_ranges': {'low': (30, 45), 'medium': (15, 29), 'high': (0, 14)}
    },
    'neck_flexion' : {  # Newly added neck flexion exercise
        'exercises_type':'neck_flexion',
        'keypoints': [0, 5, 6],  # Nose/Head, and shoulders
        'angle_function': lambda kp, shape: calculate_neck_flexion_angle(kp, shape),
        'angle_max': 45, 
        'angle_min': 5, # Max angle for full neck flexion
        'movement_threshold': 5,  # Sensitivity to detect movement
        'risk_ranges': {'low': (30, 45), 'medium': (15, 29), 'high': (0, 14)}
    },
    'neck_extension': {
        'exercises_type':'neck_extension',
        'keypoints': [0, 5, 6],  # Nose/Head, and shoulders
        'angle_function': lambda kp, shape: calculate_neck_extension_angle(kp, shape),
        'angle_max': 45,
        'angle_min': 5,  # Max angle for full neck extension
        'movement_threshold': 5,  # Sensitivity to detect movement
        'risk_ranges': {'low': (30, 45), 'medium': (15, 29), 'high': (0, 14)}
    },
    'shoulder_vertical_extension_left': {
        'exercises_type':'shoulder_vertical_extension_left',
        'keypoints': [5, 7],  # Left shoulder and left elbow
        'angle_function': lambda kp, shape: calculate_shoulder_vertical_extension (kp, shape, 'left'),
        'angle_max': 90,
        'angle_min' : 10 , # Maximum angle now 90 degrees
        'movement_threshold': 15,  # Threshold for movement
        'risk_ranges': {
            'low': (70, 90),  # Lighter risk range
            'medium': (30, 69),
            'high': (0, 29)
        }
    },
    'shoulder_vertical_extension_right': {
        'exercises_type':'shoulder_vertical_extension_right',
        'keypoints': [6, 8],  # Right shoulder and right elbow
        'angle_function': lambda kp, shape: calculate_shoulder_vertical_extension(kp, shape, 'right'),
        'angle_max': 90, 
        'angle_min' : 10, # Maximum angle now 90 degrees
        'movement_threshold': 15,  # Threshold for movement
        'risk_ranges': {
            'low': (70, 90),  # Lighter risk range
            'medium': (30, 69),
            'high': (0, 29)
        }
    },
    'shoulder_internal_rotation_left':{
        'exercises_type':'shoulder_internal_rotation_left',
        'keypoints': [5, 7, 9],  # Left shoulder, left elbow, and left hand
        'angle_function': lambda kp, shape: calculate_internal_rotation_angle(kp, shape, 'left'),
        'angle_max': 89, 
        'angle_min' : 10, # Maximum internal rotation angle
        'movement_threshold': 10,  # Movement threshold
        'risk_ranges': {
            'low': (70, 90),  # Safe range
            'medium': (30, 69),  # Medium risk
            'high': (0, 29)  # High risk
        }
    },
    'shoulder_internal_rotation_right':{
        'exercises_type':'shoulder_internal_rotation_right',
        'keypoints': [6, 8, 10],  # Left shoulder, left elbow, and left hand
        'angle_function': lambda kp, shape: calculate_internal_rotation_angle(kp, shape, 'right'),
        'angle_max': 89,
        'angle_min' : 10,  # Maximum internal rotation angle
        'movement_threshold': 10,  # Movement threshold
        'risk_ranges': {
            'low': (70, 90),  # Safe range
            'medium': (30, 69),  # Medium risk
            'high': (0, 29)  # High risk
        }
    },
    'shoulder_external_rotation_left': {
        'exercises_type':'shoulder_external_rotation_left',
        'keypoints': [5, 7, 9],  # Left shoulder, left elbow, left hand
        'angle_function': lambda kp, shape:calculate_external_rotation_angle(kp, shape, 'left'),
        'angle_max': 89, 
        'angle_min' : 10, # Max angle for external rotation
        'movement_threshold': 10,
        'risk_ranges': {
            'low': (70, 90),
            'medium': (30, 69),
            'high': (0, 29)
        }
    },

    'shoulder_external_rotation_right': {
        'exercises_type':'shoulder_external_rotation_right',
        'keypoints': [6, 8, 10],  # Right shoulder, right elbow, right hand
        'angle_function': lambda kp, shape: calculate_external_rotation_angle(kp, shape, 'right'),
        'angle_max': 89, 
        'angle_min' : 10, # Max angle for external rotation
        'movement_threshold': 10,
        'risk_ranges': {
            'low': (70, 90),
            'medium': (30, 69),
            'high': (0, 29)
        }
    },
    'hip_external_rotation_left': {
        'exercises_type':'hip_external_rotation_left',
        'keypoints': [11, 13, 15],  # Left hip, left knee, left ankle
        'angle_function': lambda kp, shape: calculate_hip_rotation_external_angle(kp, shape, 'left'),
        'angle_max': 89,  
        'angle_min' : 10, # حداکثر زاویه چرخش هیپ
        'movement_threshold': 10,  # حداقل مقدار تغییر زاویه برای ثبت حرکت
        'risk_ranges': {
            'low': (70, 90),  # ریسک پایین
            'medium': (30, 69),  # ریسک متوسط
            'high': (0, 29)  # ریسک بالا
        }
    },
    'hip_external_rotation_right': {
        'exercises_type':'hip_external_rotation_right',
        'keypoints': [12, 14, 16],  # Left hip, left knee, left ankle
        'angle_function': lambda kp, shape: calculate_hip_rotation_external_angle(kp, shape, 'right'),
        'angle_max': 89, 
        'angle_min' : 10, # حداکثر زاویه چرخش هیپ
        'movement_threshold': 10,  # حداقل مقدار تغییر زاویه برای ثبت حرکت
        'risk_ranges': {
            'low': (70, 90),  # ریسک پایین
            'medium': (30, 69),  # ریسک متوسط
            'high': (0, 29)  # ریسک بالا
        }
    },
    'hip_internal_rotation_left': {
        'exercises_type':'hip_internal_rotation_left',
        'keypoints': [11, 13, 15],  # Left hip, left knee, and left ankle
        'angle_function': lambda kp, shape: calculate_hip_rotation_internal_angle(kp, shape, 'internal', 'left'),
        'angle_max': 89, 
        'angle_min' : 10, # Maximum internal rotation angle
        'movement_threshold': 10,  # Threshold to detect meaningful movement
        'risk_ranges': {
            'low': (70, 90),  # Low risk, full mobility
            'medium': (30, 69),  # Medium risk
            'high': (0, 29)  # High risk, restricted mobility
        }
    },
    'hip_internal_rotation_right': {
        'exercises_type':'hip_internal_rotation_right',
        'keypoints': [12, 14, 16],  # Left hip, left knee, and left ankle
        'angle_function': lambda kp, shape: calculate_hip_rotation_internal_angle(kp, shape, 'internal', 'right'),
        'angle_max': 89,
        'angle_min': 10,  # Maximum internal rotation angle
        'movement_threshold': 10,  # Threshold to detect meaningful movement
        'risk_ranges': {
            'low': (70, 90),  # Low risk, full mobility
            'medium': (30, 69),  # Medium risk
            'high': (0, 29)  # High risk, restricted mobility
        }
    },
    'back_left_rotation':{
        'exercises_type':'back_left_rotation',
        'keypoints': [5, 6, 11, 12],  # Left shoulder, right shoulder, left hip, right hip
        'angle_function': lambda kp, shape: calculate_torso_rotation_angle(kp, shape, 'left'),
        'angle_max': 90, 
        'angle_min' : 10, # Maximum rotation angle for safe range
        'movement_threshold': 10,  # Threshold to detect meaningful movement
        'risk_ranges': {
            'low': (60, 90),  # Low risk, full mobility
            'medium': (30, 59),  # Medium risk
            'high': (0, 29)  # High risk, restricted mobility
        }
    },
    'back_right_rotation': {
        'exercises_type':'back_right_rotation',
        'keypoints': [5, 6, 11, 12],  # Left shoulder, right shoulder, left hip, right hip
        'angle_function': lambda kp, shape: calculate_torso_rotation_angle(kp, shape, 'right'),
        'angle_max': 90,  # Maximum rotation angle for safe range
        'angle_min' : 10,
        'movement_threshold': 10,  # Threshold to detect meaningful movement
        'risk_ranges': {
            'low': (60, 90),  # Low risk, full mobility
            'medium': (30, 59),  # Medium risk
            'high': (0, 29)  # High risk, restricted mobility
        }
    },
        'left_rotation':{
        'exercises_type':'left_rotation',
        'keypoints': [5, 6, 11, 12],  # Left shoulder, right shoulder, left hip, right hip
        'angle_function': lambda kp, shape: calculate_torso_rotation_angle(kp, shape, 'left'),
        'angle_max': 90, 
        'angle_min' : 10, # Maximum rotation angle for safe range
        'movement_threshold': 10,  # Threshold to detect meaningful movement
        'risk_ranges': {
            'low': (60, 90),  # Low risk, full mobility
            'medium': (30, 59),  # Medium risk
            'high': (0, 29)  # High risk, restricted mobility
        }
    },
    'right_rotation': {
        'exercises_type':'right_rotation',
        'keypoints': [5, 6, 11, 12],  # Left shoulder, right shoulder, left hip, right hip
        'angle_function': lambda kp, shape: calculate_torso_rotation_angle(kp, shape, 'right'),
        'angle_max': 90,
        'angle_min': 10,  # Maximum rotation angle for safe range
        'movement_threshold': 10,  # Threshold to detect meaningful movement
        'risk_ranges': {
            'low': (60, 90),  # Low risk, full mobility
            'medium': (30, 59),  # Medium risk
            'high': (0, 29)  # High risk, restricted mobility
        }
    },
    'external_rotation_left': {
        'exercises_type':'external_rotation_left',
        'keypoints': [11, 13, 15],  # Left hip, left knee, left ankle
        'angle_function': lambda kp, shape: calculate_hip_rotation_external_angle(kp, shape, 'left'),
        'angle_max': 89, 
        'angle_min' : 10, # حداکثر زاویه چرخش هیپ
        'movement_threshold': 10,  # حداقل مقدار تغییر زاویه برای ثبت حرکت
        'risk_ranges': {
            'low': (70, 90),  # ریسک پایین
            'medium': (30, 69),  # ریسک متوسط
            'high': (0, 29)  # ریسک بالا
        }
    },
    'external_rotation_right': {
        'exercises_type':'external_rotation_right',
        'keypoints': [12, 14, 16],  # Left hip, left knee, left ankle
        'angle_function': lambda kp, shape: calculate_hip_rotation_external_angle(kp, shape, 'right'),
        'angle_max': 89, 
        'angle_min' : 10, # حداکثر زاویه چرخش هیپ
        'movement_threshold': 10,  # حداقل مقدار تغییر زاویه برای ثبت حرکت
        'risk_ranges': {
            'low': (70, 90),  # ریسک پایین
            'medium': (30, 69),  # ریسک متوسط
            'high': (0, 29)  # ریسک بالا
        }
    },
    'internal_rotation_left': {
        'exercises_type':'internal_rotation_left',
        'keypoints': [11, 13, 15],  # Left hip, left knee, and left ankle
        'angle_function': lambda kp, shape: calculate_hip_rotation_internal_angle(kp, shape, 'internal', 'left'),
        'angle_max': 89, 
        'angle_min': 10, # Maximum internal rotation angle
        'movement_threshold': 10,  # Threshold to detect meaningful movement
        'risk_ranges': {
            'low': (70, 90),  # Low risk, full mobility
            'medium': (30, 69),  # Medium risk
            'high': (0, 29)  # High risk, restricted mobility
        }
    },
    'internal_rotation_right': {
        'exercises_type':'internal_rotation_right',
        'keypoints': [12, 14, 16],  # Left hip, left knee, and left ankle
        'angle_function': lambda kp, shape: calculate_hip_rotation_internal_angle(kp, shape, 'internal', 'right'),
        'angle_max': 89, 
        'angle_min': 10, # Maximum internal rotation angle
        'movement_threshold': 10,  # Threshold to detect meaningful movement
        'risk_ranges': {
            'low': (70, 90),  # Low risk, full mobility
            'medium': (30, 69),  # Medium risk
            'high': (0, 29)  # High risk, restricted mobility
        },
    },
    'knee_raise_hip_left': {
        'exercises_type':'knee_raise_hip_left',
        'keypoints': [11, 13],
        'angle_function': lambda kp, shape: calculate_knee_raise_angle(kp, shape, 'left'),
        'angle_max': 120,
        'angle_min' : 10,
        'movement_threshold': 15,
        'risk_ranges': {'low': (91, 120), 'medium': (50, 90), 'high': (0, 49)}
    },
    'knee_raise_hip_right': {
        'exercises_type':'knee_raise_hip_right',
        'keypoints': [12, 14],
        'angle_function': lambda kp, shape: calculate_knee_raise_angle(kp, shape, 'right'),
        'angle_max': 120,
        'angle_min' : 10,
        'movement_threshold': 15,
        'risk_ranges': {'low': (91, 120), 'medium': (50, 90), 'high': (0, 49)}
    }

}
SECRET_KEY = "255621@G320dQq@#"  # Make this a strong secret key
# 9jan25