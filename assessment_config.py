
ASSESSMENT_CONFIG = {
    "back": {
        "charts": [
            {
                "chart_title": "back analysis",
                "chart_type": "bar",
                "body_parts": ["flexion", "extension", "lateral_flexion", "rotation"]
          

            },
            {
                "chart_title": "hip and knee analysis",
                "chart_type": "bar",
                "body_parts": ["hip_internal_rotation", "hip_external_rotation", "knee_flexion"]
           
            }
        ],
        "table_movements": {
            "back_flexion": 90,
            "back_extension": 30,
            "lateral_flexion": 40,
            "back_left_rotation": 60,
            "back_right_rotation": 60,
            "knee_raise_left": 130,
            "knee_raise_right": 130,
            "hip_internal_rotation_left": 90,
            "hip_internal_rotation_right": 90,
            "hip_external_rotation_left": 90,
            "hip_external_rotation_right": 90
        }
    },
    "full_body": {
        "charts": [
            {
                "chart_title": "back analysis",
                "chart_type": "bar",
                "body_parts": ["flexion", "extension", "lateral_flexion"]

            },
            {
                "chart_title": "knee and shoulder analysis",
                "chart_type": "bar",
                "body_parts": ["knee_flexion", "shoulder_vertical_flexion", "shoulder_abduction"]
            }
        ],
        "table_movements": {
            "back_flexion": 90,
            "back_extension": 30,
            "lateral_flexion": 40,
            "knee_raise_left": 130,
            "knee_raise_right": 130,
            "shoulder_vertical_flexion_left": 180,
            "shoulder_vertical_flexion_right": 180,
            "shoulder_abduction": 180
        }
    },
    "neck_shoulder": {
        "charts": [
            {
                "chart_title": "neck analysis",
                "chart_type": "bar",
                "body_parts": ["flexion", "extension", "tilt", "rotation"]
            },
            {
                "chart_title": "shoulder analysis",
                "chart_type": "bar",
                "body_parts": ["abduction", "internal_rotation", "external_rotation", "vertical_flexion"]
            }
        ],
        "table_movements": {
            "neck_flexion": 60,
            "neck_extension": 75,
            "neck_left_tilt": 50,
            "neck_right_tilt": 50,
            "neck_rotation_stretch_left": 90,
            "neck_rotation_stretch_right": 90,
            "shoulder_abduction": 180,
            "shoulder_internal_rotation_left": 90,
            "shoulder_internal_rotation_right": 90,
            "shoulder_external_rotation_left": 90,
            "shoulder_external_rotation_right": 90,
            "shoulder_vertical_flexion_left": 180,
            "shoulder_vertical_flexion_right": 180
        }
    }
}

STATUS_COLOR_MAP = {
    "Good": "green",
    "Fair": "orange",
    "Poor": "red"
}
