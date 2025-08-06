
ASSESSMENT_CONFIG = {
    "back": {
        "charts": [
            {
                "chart_title": "back analysis",
                "chart_type": "bar",
                "body_parts": {"flexion" : ["back_flexion"], "extension": ["back_extension"], "lateral_flexion" : ["lateral_flexion"], "rotation":["back_left_rotation","back_right_rotation"]}
            },
            {
                "chart_title": "hip and knee analysis",
                "chart_type": "bar",
                "body_parts": {"hip_internal_rotation":["hip_internal_rotation_left","hip_internal_rotation_right"], "hip_external_rotation":["hip_external_rotation_left","hip_external_rotation_right"], "knee_flexion":["knee_raise_left","knee_raise_right"]}
           
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
                "body_parts": {"flexion" : ["back_flexion"], "extension": ["back_extension"], "lateral_flexion" : ["lateral_flexion"], "rotation":["back_left_rotation","back_right_rotation"]}

            },
            {
                "chart_title": "knee and shoulder analysis",
                "chart_type": "bar",
                "body_parts": { "knee_flexion":["knee_raise_left","knee_raise_right"], "shoulder_vertical_flexion" : ["shoulder_vertical_flexion_left","shoulder_vertical_flexion_right"], "shoulder_abduction":["shoulder_abduction"]}
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
    "shoulder_and_neck": {
        "charts": [
            {
                "chart_title": "neck analysis",
                "chart_type": "bar",
                "body_parts": {"flexion": ["neck_flexion"] , "extension" :["neck_extension"] , "tilt":["neck_left_tilt","neck_right_tilt"]}
            },
            {
                "chart_title": "shoulder analysis",
                "chart_type": "bar",
                "body_parts": {"abduction":["shoulder_abduction"], "internal_rotation":["shoulder_internal_rotation_left","shoulder_internal_rotation_right"], "external_rotation":["shoulder_external_rotation_left","shoulder_external_rotation_right"], "vertical_flexion":["shoulder_vertical_flexion_left","shoulder_vertical_flexion_right"]}
            }
        ],
        "table_movements": {
            "neck_flexion": 60,
            "neck_extension": 75,
            "neck_left_tilt": 50,
            "neck_right_tilt": 50,
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
