import cv2
import numpy as np
import firebase_admin
import os
import io
import json
from firebase_admin import credentials, firestore
from datetime import datetime
from google.cloud import vision

# Initialize Cloud Vision API and Firebase Admin SDK
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_vision.json'
cred = credentials.Certificate("ServiceAccountKey.json")
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

# Parking Records Collection
parking_records_collection = db.collection(u'parking_records')

# Car Plate Numbers Collection
car_plate_uid_docs = db.collection(u'car_plate_numbers').get()


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
        if len(text.description) == 4:
            # print(text.description)
            return text.description

    # [END vision_python_migration_text_detection]
# [END vision_text_detection]


# For canny detection, translate the frame to grayscale and to canny edge detection
# then detect the status of occupancy
car_threshold_value = 1000
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = auto_canny(blurred)
    canny_value = cv2.countNonZero(canny)
    # print(canny_value)

    # For debugging purpose. Checks onto cloud vision api and Firestore
    # k = cv2.waitKey(1)
    # if k%256 == 32:
    #     img_name = "enter_car.jpg"
    #     cv2.imwrite(img_name, frame)
    #     car_plate_number = detect_text("enter_car.jpg")
    #     print(car_plate_number)
    #
    #     # Check the car plate number is registed or not in existing user
    #     # Find car plate numbers in car_plate_collection of UID document
    #     for doc in car_plate_uid_docs:
    #         # See json.dumps() as a save method
    #         # See json.loads() as a retrieve method
    #         json_dump = json.dumps(doc.to_dict())
    #         json_load = json.loads(json_dump)
    #
    #         for value in json_load['plate_numbers']:
    #             if value == car_plate_number:
    #                 # found car plate numbers of UID document
    #                 data = {
    #                     u'UID': doc.id,
    #                     u'plate_number': car_plate_number,
    #                     u'date': '',
    #                     u'start_time': datetime.time(datetime.now().replace(microsecond=0)).isoformat(),
    #                     u'end_time': '',
    #                     u'duration': '',
    #                     u'space': '',
    #                     u'paid_parking_fee': ''
    #                 }
    #                 parking_records_collection.add(data)
    #
    #                 # For Debugging purpose. Display the json value
    #                 # print(doc.id)
    #                 # print(car_plate_number)
    #                 # print(datetime.time(datetime.now().replace(microsecond=0)))

    if canny_value > car_threshold_value:
        # Means got car
        # print("got enter car")
        cv2.imwrite("enter_car.jpg", frame)
        car_plate_number = detect_text("enter_car.jpg")
        print(car_plate_number)

        # Check the car plate number is registed or not in existing user
        # Find car plate numbers in car_plate_collection of UID document
        for doc in car_plate_uid_docs:
            # See json.dumps() as a save method
            # See json.loads() as a retrieve method
            json_dump = json.dumps(doc.to_dict())
            json_load = json.loads(json_dump)

            for value in json_load['plate_numbers']:
                if value == car_plate_number:
                    # found car plate numbers of UID document
                    data = {
                        u'UID': doc.id,
                        u'plate_number': car_plate_number,
                        u'date': '',
                        u'start_time': datetime.time(datetime.now().replace(microsecond=0)).isoformat(),
                        u'end_time': '',
                        u'duration': '',
                        u'space': '',
                        u'paid_parking_fee': ''
                    }
                    parking_records_collection.add(data)
            print("Open Barrier")
            print("Close Barrier")

    cv2.imshow('Final Outcome', frame)
    cv2.imshow('canny', canny)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()




