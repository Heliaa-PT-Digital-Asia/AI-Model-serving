from flask import Flask, request, jsonify
import pandas as pd
from config import exercise_config
from angle_functions import determine_risk
import uuid
import sqlite3
import json


app = Flask(__name__)

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

# Initialize the database
init_db()

# Register user route
@app.route('/register', methods=['POST'])
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
def save_results_to_db(user_uuid,  exercise_type , average_angle, risk_label, top_12_angles):
    conn = sqlite3.connect('AI_DB.db')
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS results (
        user_uuid TEXT,
        exercise_type TEXT,
        average_angle REAL,
        risk_label TEXT,
        top_12_angles TEXT
    )
    ''')
    
    # Insert the result into the table
    cursor.execute('''
    INSERT INTO results (user_uuid, exercise_type, average_angle, risk_label, top_12_angles)
    VALUES (?, ?, ?, ?, ?)
    ''', (user_uuid, exercise_type, average_angle, risk_label, json.dumps(top_12_angles)))
    
    conn.commit()
    conn.close()

@app.route('/calculate-angle', methods=['POST'])
def calculate_angle():
    data = request.json
    if 'meta' not in data or 'content' not in data or 'userUUID' not in data:
        return jsonify({"error": "Invalid JSON structure"}), 400

    user_uuid = data['userUUID']  # Get the userUUID from the request
    frame_shape = (data['meta']['frame_shape']['y'], data['meta']['frame_shape']['x'])
    keypoints_data = data['content']
    exercise_type = data['meta']['exercise_type']
    angles_data = []
    config = exercise_config[exercise_type]

    for frame in keypoints_data:
        keypoints = frame['data']
        if len(keypoints) > 0:
            dict_keypoints = {kp['id']: kp for kp in keypoints}
            if len(dict_keypoints.keys()) == len(config['keypoints']):
                angle = config['angle_function'](dict_keypoints, frame_shape)
        else:
            angle = 0

        if 0 < angle < config['angle_max']:
            angles_data.append({
                'Time': frame['time'],
                'Angle': angle
            })

    df = pd.DataFrame(angles_data)
    if not df.empty:
        df = df.nlargest(12, 'Angle')
        average_angle = df['Angle'].mean()
        top_12_angles = df[['Time', 'Angle']].to_dict(orient='records')

        risk_label = determine_risk(average_angle, config['risk_ranges'])

        # Store the results in the database, associating them with the userUUID
        save_results_to_db(user_uuid,  exercise_type, average_angle, risk_label, top_12_angles)

    else:
        # Still save an error to the database if no valid angles found
        save_results_to_db(user_uuid, None, "No valid angles found", [])

    # Return response after storing the data
    return jsonify({"message": "done"})


@app.route('/get-calculated-data', methods=['POST'])
def get_calculated_data():
    data = request.json
    user_uuid = data.get('userUUID')
    
    if not user_uuid:
        return jsonify({"error": "Missing userUUID"}), 400
    
    # Query the database to retrieve data for this userUUID
    conn = sqlite3.connect('AI_DB.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT exercise_type, average_angle, risk_label, top_12_angles 
    FROM results 
    WHERE user_uuid = ?
    ''', (user_uuid,))
    
    results = cursor.fetchall()
    conn.close()
    
    if results:
        exercises_data = []
        for row in results:
            exercise_type, average_angle, risk_label, top_12_angles = row
            top_12_angles = json.loads(top_12_angles)  # Convert back from JSON to Python list
            
            # Extract only the angle values, ignore the time
            angle_values = [entry['Angle'] for entry in top_12_angles]
            
            exercises_data.append({
                "exercise_type": exercise_type,
                "average_angle": average_angle,
                "risk_label": risk_label,
                "angles": angle_values
            })
        
        response = {
            "userUUID": user_uuid,
            "exercises": exercises_data
        }
    else:
        response = {"error": "No data found for the given userUUID"}
    
    return jsonify(response)




@app.route('/delete-user', methods=['POST'])
def delete_user():
    data = request.json
    user_uuid = data.get('userUUID')

    if not user_uuid:
        return jsonify({"message": "userUUID is missing"}), 400

    # Delete from users.db
    conn_db = sqlite3.connect('AI_DB.db')
    cursor = conn_db.cursor()
    cursor.execute('DELETE FROM users WHERE userUUID= ?', (user_uuid,))
    cursor.execute('DELETE FROM results WHERE user_uuid = ?', (user_uuid,))
    conn_db.commit()
    deleted_from_ai = cursor.rowcount > 0  # Check if any row was deleted
    conn_db.close()

    # Check if the user existed in either DB
    if deleted_from_ai:
        return jsonify({"message": "deleted"}), 200
    else:
        return jsonify({"message": "user not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
