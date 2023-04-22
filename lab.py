import cv2
import numpy as np
import tensorflow as tf
import keras
from mrcnn import model as modellib, utils
from mrcnn.config import Config

# Define the Mask R-CNN configuration
class MaskRCNNConfig(Config):
    NAME = "MaskRCNN"
    IMAGES_PER_GPU = 1
    NUM_CLASSES = 2  # background + person
    DETECTION_MIN_CONFIDENCE = 0.9

# Create the Mask R-CNN model
model = modellib.MaskRCNN(mode="inference", config=MaskRCNNConfig(), model_dir='./')

# Load the trained weights
model_path = "./mask_rcnn_balloon.h5"
model.load_weights(model_path, by_name=True)

# Load the image
image = cv2.imread('path/to/image.jpg')

# Convert the image to RGB format
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Run the detection
results = model.detect([image], verbose=0)

# Extract the person's mask
mask = results[0]['masks'][:, :, 0]

# Extract the person's body and clothing region
person_image = np.zeros_like(image)
person_image[:, :, 0] = image[:, :, 0] * mask
person_image[:, :, 1] = image[:, :, 1] * mask
person_image[:, :, 2] = image[:, :, 2] * mask
