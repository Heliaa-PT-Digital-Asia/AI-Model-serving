from flask import Flask, request, jsonify
import cv2
import numpy as np
from model_utils import load_model_from_s3, run_inference

app = Flask(__name__)

# Assuming the model is stored in AWS S3
BUCKET_NAME = 'ai-detection-model'
MODEL_KEY = 'main-model/'

model = None

@app.route('/load_model', methods=['GET'])
def load_model():
    global model
    model = load_model_from_s3(BUCKET_NAME, MODEL_KEY, '')
    if model:
        return jsonify({'message': 'Model loaded successfully'}), 200
    else:
        return jsonify({'message': 'Failed to load model'}), 500

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model is not loaded'}), 400
    
    file = request.files['file']
    npimg = np.fromstring(file.read(), np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    keypoints = run_inference(model, frame)
    return jsonify({'keypoints': keypoints}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

