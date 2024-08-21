import tensorflow as tf
import cv2
import numpy as np
import boto3
# from botocore.exceptions import NoCredentialsError

# def load_model_from_s3(bucket_name, model_key, local_path='local_model'):
#     s3 = boto3.client('s3')
#     try:
#         s3.download_file(bucket_name, model_key, local_path)
#         print("Model downloaded successfully from S3.")
#     except NoCredentialsError:
#         print("Credentials not available.")
#         return None
#     return tf.saved_model.load(local_path)

from botocore.exceptions import NoCredentialsError, ClientError

def load_model_from_s3(bucket_name, model_key, local_path):
    s3 = boto3.client('s3')
    s3_path = f"s3://{bucket_name}/{model_key}"

    try:
        print(f"Attempting to download model from {s3_path}...")
        s3.download_file(bucket_name, model_key, local_path)
        print(f"Model downloaded successfully from {s3_path} to {local_path}.")
    except NoCredentialsError:
        print("Credentials not available.")
        return None
    except ClientError as e:
        print(f"Failed to download model from {s3_path}. Error: {e}")
        return None

    # Load the TensorFlow model from the local path
    try:
        model = tf.saved_model.load(local_path)
        print(f"Model loaded successfully from {local_path}.")
        return model
    except Exception as e:
        print(f"Failed to load model from {local_path}. Error: {e}")
        return None

def run_inference(model, frame):
    movenet = model.signatures['serving_default']
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_resized = tf.image.resize_with_pad(tf.expand_dims(image_rgb, axis=0), 256, 256)
    image_np = image_resized.numpy().astype(np.int32)
    outputs = movenet(tf.constant(image_np))
    keypoints = outputs['output_0'].numpy()[0][0]
    return keypoints.tolist()  # Convert numpy array to list for JSON serialization
