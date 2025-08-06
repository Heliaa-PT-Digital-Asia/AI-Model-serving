from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from config import exercise_config
from angle_functions import determine_risk
import uuid
import sqlite3
import json
from collections import Counter
from assessment_config import ASSESSMENT_CONFIG
from config import exercise_config

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST","PATCH","PUT","DELETE"]}}) # This will enable CORS for all routes

# Connect to SQLite database
def init_db():
    conn = sqlite3.connect('AI_DB.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        userId TEXT PRIMARY KEY,
        userUUID TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Function to add a new user to the SQLite DB
def register_user_in_db(user_id, user_uuid):
    conn = sqlite3.connect('AI_DB.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (userId, userUUID) VALUES (?, ?)', (user_id, user_uuid))
    conn.commit()
    conn.close()

# Function to get the UUID for a user from the SQLite DB
def get_user_uuid_from_db(user_id):
    conn = sqlite3.connect('AI_DB.db')
    cursor = conn.cursor()
    cursor.execute('SELECT userUUID FROM users WHERE userId = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def store_angle_data(user_uuid, exercise_type, angle):
    conn = sqlite3.connect('AI_DB.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO angle_data (user_uuid, exercise_type, angle, timestamp)
    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
    ''', (user_uuid, exercise_type, angle))
    conn.commit()
    conn.close()

def evaluate_performance(user_uuid, exercise_type):
    # Connect to database to fetch historical angle data
    conn = sqlite3.connect('AI_DB.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT angle, timestamp 
        FROM angle_data 
        WHERE user_uuid = ? AND exercise_type = ?
        ORDER BY timestamp DESC 
         
    ''', (user_uuid, exercise_type))

    results = cursor.fetchall()
    conn.close()

    # Check if the user failed to meet the angle threshold
    min_threshold = exercise_config[exercise_type]['angle_min']
    failures = [angle for angle, _ in results if angle < min_threshold]
    fail_count = len(failures) / (len(results))
    



    if fail_count > 0.85:  # Arbitrary threshold, can be adjusted
        return {"skip": True, "message": "You can skip this exercise."}
    else:
        return {"skip": False, "message": "Please continue trying."}

# Sample database table creation for storing angles
def init_angle_data_db():
    conn = sqlite3.connect('AI_DB.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS angle_data (
        user_uuid TEXT,
        exercise_type TEXT,
        angle REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()
# Initialize the database
init_db()
init_angle_data_db()
# Register user route
@app.route('/', methods=['POST'])
def register_user():
    data = request.json
    user_id = data.get('userId')
    if not user_id:
        return jsonify({"error": "UserId is required"}), 400

    # Check if the user is already registered
    existing_uuid = get_user_uuid_from_db(user_id)
    if existing_uuid:
        return jsonify({"userUUID": existing_uuid}), 200

    # Generate a new UUID and store it in the database
    user_uuid = str(uuid.uuid4())
    register_user_in_db(user_id, user_uuid)

    return jsonify({"userUUID": user_uuid}), 201

# Function to save results to SQLite database
def save_results_to_db(user_uuid,  exercise_type , average_angle, risk_label, best_angle ,top_12_angles, skip):
    conn = sqlite3.connect('AI_DB.db')
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS results (
        user_uuid TEXT,
        exercise_type TEXT,
        average_angle REAL,
        risk_label TEXT,
        best_angle TEXT,
        top_12_angles TEXT,
        skip TEXT
    )
    ''')
    
    # Insert the result into the table
    cursor.execute('''
    INSERT INTO results (user_uuid, exercise_type, average_angle, risk_label, best_angle, top_12_angles, skip)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_uuid, exercise_type, average_angle, risk_label, best_angle ,json.dumps(top_12_angles), skip))
    
    conn.commit()
    conn.close()



@app.route('/', methods=['PATCH'])
def calculate_angle():
    data = request.json
    if 'meta' not in data or 'content' not in data or 'userUUID' not in data:
        return jsonify({"error": "Invalid JSON structure"}), 400

    user_uuid = data['userUUID']
    frame_shape = (data['meta']['frame_shape']['y'], data['meta']['frame_shape']['x'])
    keypoints_data = data['content']
    exercise_type = data['meta']['exercise_type']
    config = exercise_config[exercise_type]
    angles_data = []

    for frame in keypoints_data:
        keypoints = frame['data']
        if len(keypoints) > 0:
            dict_keypoints = {kp['id']: kp for kp in keypoints}
            if all(kp_id in dict_keypoints for kp_id in config['keypoints']):
                angle = config['angle_function'](dict_keypoints, frame_shape)
                if 0 < angle < config['angle_max']:
                    angles_data.append({
                        'Time': frame['time'],
                        'Angle': angle
                    })

                    store_angle_data(user_uuid, exercise_type, angle)

    if angles_data:
        df = pd.DataFrame(angles_data)
        df = df.nlargest(12, 'Angle')  # Consider top 12 angles for finding the best angle
        average_angle = df['Angle'].mean()
        top_12_angles = df[['Time', 'Angle']].to_dict(orient='records')

        # Determine risk labels for each angle and find the most frequent angle within the most common risk label
        df['RiskLabel'] = df['Angle'].apply(lambda x: determine_risk(x, config['risk_ranges']))
        most_common_label = df['RiskLabel'].mode()[0]
        df['Angle'] = df['Angle'].astype(int)
        best_angle = df[df['RiskLabel'] == most_common_label]['Angle'].value_counts().idxmax()

        risk_label = determine_risk(average_angle, config['risk_ranges'])

        # Store the results in the database, associating them with the userUUID
        
        skipping_response = evaluate_performance(user_uuid, exercise_type)
        save_results_to_db(user_uuid, exercise_type, average_angle, risk_label, float (best_angle) , top_12_angles, skipping_response['skip'])
        return jsonify({
            "userUUID": user_uuid,
            "average_angle": average_angle,
            "best_angle": float (best_angle),
            "risk_label": risk_label,
            "top_angles": top_12_angles,
            "skip": skipping_response['skip'],
            "message": skipping_response['message']
        })
 
    else:
        # Still save an error to the database if no valid angles found
        save_results_to_db(user_uuid, exercise_type, 0.0 , "High Risk" ,0.0, [],True)
        return jsonify({"error": "No valid angles found"})

@app.route('/', methods=['GET'])
def get_calculated_data():
    data = request.json
    user_uuid = data.get('userUUID')
    
    if not user_uuid:
        return jsonify({"error": "Missing userUUID"}), 400
    
    # Query the database to retrieve data for this userUUID
    conn = sqlite3.connect('AI_DB.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT exercise_type, average_angle, risk_label, top_12_angles , best_angle, skip
    FROM results 
    WHERE user_uuid = ?
    ''', (user_uuid,))
    
    results = cursor.fetchall()
    conn.close()
    
    if results:
        exercises_data = []
        total_risk_amount = 0  
        num_exercises = 0 
        # To calculate the total risk amount
        # num_exercises = len(results)  # Count the number of exercises

        for row in results:
            exercise_type, average_angle, risk_label, top_12_angles, best_angle , skip = row
            top_12_angles = json.loads(top_12_angles)  # Convert back from JSON to Python list
            
            # Extract only the angle values, ignore the time
            angle_values = [entry['Angle'] for entry in top_12_angles]

            # Get the risk ranges from the exercise configuration
            config = exercise_config.get(exercise_type)
            if config:
                risk_ranges = config['risk_ranges']
                angle_max = config['angle_max']

                # Dynamic calculation of risk amount based on normalized value
                exercise_risk_amounts = []
                for angle in angle_values:
                    if risk_ranges['low'][0] <= angle <= risk_ranges['low'][1]:
                        # Low risk - Map to the range of 0 to 3
                        normalized_value = (angle - risk_ranges['low'][0]) / (risk_ranges['low'][1] - risk_ranges['low'][0])
                        exercise_risk_amounts.append(normalized_value * 3)
                    elif risk_ranges['medium'][0] <= angle <= risk_ranges['medium'][1]:
                        # Medium risk - Map to the range of 3 to 6
                        normalized_value = (angle - risk_ranges['medium'][0]) / (risk_ranges['medium'][1] - risk_ranges['medium'][0])
                        exercise_risk_amounts.append(3 + normalized_value * 3)
                    elif risk_ranges['high'][0] <= angle <= risk_ranges['high'][1]:
                        # High risk - Map to the range of 6 to 8
                        normalized_value = (angle - risk_ranges['high'][0]) / (risk_ranges['high'][1] - risk_ranges['high'][0])
                        exercise_risk_amounts.append(6 + normalized_value * 2)
                    else:
                        exercise_risk_amounts.append(0)  # Out of range (error case)
                if skip == "0": 
                    exercise_risk_amount = sum ( exercise_risk_amounts) / len (exercise_risk_amounts )                  
                    total_risk_amount += exercise_risk_amount  # Sum for calculating the average
                    num_exercises = num_exercises + 1 


                exercises_data.append({
                    "exercise_key": exercise_type,
                    "average_angle": average_angle,
                    "risk_label": risk_label,
                    "angles": angle_values,
                    "best_angle": best_angle,
                    "skip": skip
                })

        # Calculate the total risk amount (average risk across all exercises)
        total_risk_amount = total_risk_amount / num_exercises if num_exercises > 0 else 100

        # Determine the total risk level based on the total risk amount
        if total_risk_amount <= 2.99:
            total_risk_level = "Low Risk"
        elif 3 <= total_risk_amount <= 4.99:
            total_risk_level = "Medium Risk"
        else:
            total_risk_level = "High Risk"
        
        response = {
            "userUUID": user_uuid,
            "exercises": exercises_data,
            "total_risk_amount": total_risk_amount,
            "total_risk_level": total_risk_level
        }
    else:
        response = {"error": "No data found for the given userUUID"}
    
    return jsonify(response)


@app.route('/', methods=['DELETE'])
def delete_user():
    data = request.json
    user_uuid = data.get('userUUID')

    if not user_uuid:
        return jsonify({"message": "userUUID is missing"}), 200

    conn_db = sqlite3.connect('AI_DB.db')
    cursor = conn_db.cursor()

    # Check if the 'users' table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    if not cursor.fetchone():
        return jsonify({"message": "Users table does not exist"}), 200

    # Check if the 'results' table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='results';")
    if not cursor.fetchone():
        return jsonify({"message": "Results table does not exist"}), 200

    # Proceed with the deletion if tables exist
    cursor.execute('DELETE FROM users WHERE userUUID= ?', (user_uuid,))
    cursor.execute('DELETE FROM results WHERE user_uuid = ?', (user_uuid,))
    cursor.execute('DELETE FROM angle_data WHERE user_uuid = ?', (user_uuid,))
    conn_db.commit()

    deleted_from_ai = cursor.rowcount > 0  # Check if any row was deleted
    conn_db.close()

    if deleted_from_ai:
        return jsonify({"message": "User and results deleted successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 200



@app.route('/drop', methods=['DELETE'])
def delete_results():
    data = request.json
    user_uuid = data.get('userUUID')

    if not user_uuid:
        #400
        return jsonify({"message": "userUUID is missing"}), 200

    # Connect to the AI_DB.db to delete only from the results table
    conn_db = sqlite3.connect('AI_DB.db')
    cursor = conn_db.cursor()

    # Check if the 'results' table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='results';")
    if not cursor.fetchone():
        #500
        return jsonify({"message": "Results table does not exist"}), 200

    # Delete the results associated with this userUUID from the results table
    cursor.execute('DELETE FROM results WHERE user_uuid = ?', (user_uuid,))
    
    deleted_from_results = cursor.rowcount > 0  # Check if any row was deleted
    cnt=cursor.rowcount
    cursor.execute('DELETE FROM angle_data WHERE user_uuid = ?', (user_uuid,))
    conn_db.commit()
    conn_db.close()

    if deleted_from_results:
        return jsonify({"Affected rows": cnt}), 200
        
    else:
        #404
        return jsonify({"message": "No results found for the given userUUID"}), 200

# Mapping of body parts to exercises
# This mapping is used to determine which exercises correspond to each body part in the assessment charts


def fetch_user_exercises(user_uuid):
    conn = sqlite3.connect('AI_DB.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT exercise_type, CAST(best_angle AS FLOAT)
        FROM results
        WHERE user_uuid = ? AND skip = 0
    """, (user_uuid,))
    rows = cursor.fetchall()
    conn.close()
    return {exercise: avg for exercise, avg in rows}

correction_map = { "lateral_left_right_tilt" : "lateral_flexion" , "left_rotation" : "back_left_rotation", "right_rotation": "back_right_rotation" ,"internal_rotation_left": "hip_internal_rotation_left", 
 "internal_rotation_right": "hip_internal_rotation_right", "external_rotation_left": "hip_external_rotation_left", "external_rotation_right": "hip_external_rotation_right",
  "knee_raise_hip_left": "knee_raise_left", "knee_raise_hip_right": "knee_raise_right","right_shoulder_vertical_flexion": "shoulder_vertical_flexion_right", "left_shoulder_vertical_flexion": "shoulder_vertical_flexion_left",
  "right_tilt": "neck_right_tilt","left_tilt": "neck_left_tilt"}


# === Main Summary Generator ===
def generate_assessment_summary(user_uuid, assessment_name):
    assessment = ASSESSMENT_CONFIG.get(assessment_name)
    if not assessment:
        return {"error": "Invalid assessment name"}

    user_data = fetch_user_exercises(user_uuid)
    print ("User Data v1:", user_data)
    charts_output = []
    table_output = []
    all_status_values = []


    corrected_user_data = {}
    for key, value in user_data.items():
        new_key = correction_map.get(key, key)  
        corrected_user_data[new_key] = value
    user_data = corrected_user_data
    print ("User Data:", user_data)


    for chart in assessment["charts"]:
        body_detail = {}
        for part, mapped_exercises in chart["body_parts"].items():
            # mapped_exercises = chart_to_exercises_mapping.get(part, [])
            relevant_angles = [user_data[ex] for ex in mapped_exercises if ex in user_data]

            if relevant_angles:
                avg_angle = sum(relevant_angles) / len(relevant_angles)
                normal_range_values = []
                for ex in mapped_exercises:
                    for move_key, norm in assessment["table_movements"].items():
                        if ex == move_key:
                            normal_range_values.append(norm)
                if normal_range_values:
                    avg_normal = sum(normal_range_values) / len(normal_range_values)
                else:
                    avg_normal = 1  
                percent = avg_angle / avg_normal
                if percent >= 0.75:
                    status = "good"
                elif percent >= 0.5:
                    status = "fair"
                else:
                    status = "poor"
            else:
                status = "poor"

            body_detail[part] = status
            all_status_values.append(status)

        charts_output.append({
            "chart_title": chart["chart_title"],
            "chart_type": chart["chart_type"],
            "body_detail": body_detail
        })

    # Generate the table output based on the assessment movements
    for movement, normal_range in assessment["table_movements"].items():
        result_angle = user_data.get(movement, 0)
        percent = result_angle / normal_range if normal_range > 0 else 0
        if percent >= 0.75:
            color = "green"
        elif percent >= 0.5:
            color = "orange"
        else:
            color = "red"

        table_output.append({
            "movment": movement,
            "result": round(result_angle, 1),
            "normal_range": normal_range,
            "color": color
        })

    
    from collections import Counter
    most_common = Counter(all_status_values).most_common(1)
    overall_status = most_common[0][0] if most_common else "poor"

    return {
        "userUUID": user_uuid,
        "assessment": assessment_name,
        "overall": overall_status,
        "charts": charts_output,
        "table": table_output
    }

# === Main API Endpoint ===
@app.route('/api/assessment_summary', methods=['POST'])
def get_chart_assessment():
    data = request.get_json()
    user_uuid = data.get("userUUID")
    assessment_name = data.get("assessment")

    if not user_uuid or not assessment_name:
        return jsonify({"error": "Missing userUUID or assessment"}), 400

    summary = generate_assessment_summary(user_uuid, assessment_name)
    return jsonify(summary)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)