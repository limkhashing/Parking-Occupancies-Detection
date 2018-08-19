import cv2
import numpy as np
import firebase_admin
import io
import os
import time
from firebase_admin import credentials, firestore
from google.cloud import vision
from datetime import datetime

# TODO firebase firestore initialization
# TODO car plate number detection check


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
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    # [END vision_python_migration_text_detection]
# [END vision_text_detection]


car_threshold_value = 5000
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
while True:
    ret, frame = cap.read()
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # float
    print(height)
    print(width)
    # For canny detection, translate the frame to grayscale
    # then detect the status of occupancy
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = auto_canny(blurred)

    canny_value = cv2.countNonZero(canny)
    print(canny_value)
    # TODO change detection value accordingly
    if (canny_value > car_threshold_value):
        # Means got car
        print("got exit car")
        cv2.imwrite("exit_car.jpg", frame)
        # detect_text("exit_car.jpg")
        # TODO check detected OCR. Must minimum 4 characters
        # TODO Check parking record db exist user, got enter time and no exit time

        # if true, send exit time
        # Calculate payment fees
        # Auto pay
        # after pay, open barrier, delay 4 second, close barrier
        print(datetime.time(datetime.now().replace(microsecond=0)))
        print("Open Barrier")
        # time.sleep(4)
        print("Close Barrier")

    cv2.imshow('Final Outcome', frame)
    cv2.imshow('canny', canny)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()




