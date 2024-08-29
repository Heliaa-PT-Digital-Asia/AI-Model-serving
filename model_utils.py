import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np

def load_model():
    model = hub.load("https://tfhub.dev/google/movenet/singlepose/thunder/4")
    # model = model.signatures['serving_default']
    # model = tf.saved_model.load(model_path)
    print('model-loaded')
    return model

def run_inference(model, frame):
    # Assuming 'serving_default' is available in the model
    movenet = model.signatures['serving_default']
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_resized = tf.image.resize_with_pad(tf.expand_dims(image_rgb, axis=0), 256, 256)
    image_np = image_resized.numpy().astype(np.int32)
    outputs = movenet(tf.constant(image_np))
    keypoints = outputs['output_0'].numpy()
    return keypoints[0][0]
