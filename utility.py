import cv2
import os
import numpy as np
import io
import time
from google.cloud import vision

# MySql / PhpMyAdmin Connection Variable
host = u'sql132.main-hosting.eu'
user = u'u824500046_fyp'
pw = u'7pmfyvTNvyeU'
db = u'u824500046_fyp'

# Initialize Cloud Vision API and Firebase Admin SDK
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_vision.json'


# [START vision_text_detection]
def detect_text(frame):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    # [START vision_python_migration_text_detection]
    with io.open(frame, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    for text in texts:
        if len(text.description) == 4:
            # print(text.description)
            return text.description


# Function that return canny detection
def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    # In practice, sigma=0.33  tends to give good results on most of the dataset
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged
    # [END vision_python_migration_text_detection]
# [END vision_text_detection]
