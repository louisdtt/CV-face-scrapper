# Handling imports
import cv2
import os
import numpy as np

# Paths
base_dir = os.path.dirname(__file__)
prototxt_path = os.path.join(base_dir + 'model_data/deploy.prototxt')
caffemodel_path = os.path.join(base_dir + 'model_data/weights.caffemodel')

# Read the model
model = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)

# Create directory 'updated_images' if it does not exist
if not os.path.exists('updated_images'):
    print("New directory created")
    os.makedirs('updated_images')

if not os.path.exists('faces'):
    print("New directory created")
    os.makedirs('faces')

# Loop through images
for file in os.listdir(base_dir + 'images'):
    file_name, file_extension = os.path.splitext(file)
    if (file_extension in ['.png','jpg']):
        print("Image path: {}".format(base_dir + 'images/' + file))

# Detect faces
image = cv2.imread(base_dir + 'images/' + file)

(h,w) = image.shape[:2]
blob = cv2.dnn.blobFromImage(cv2.resize(image,(300,300)),1.0,(300,300),(104.0,177.0,123.0))

model.setInput(blob)
detections = model.forward()