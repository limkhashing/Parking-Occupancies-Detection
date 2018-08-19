import cv2
import numpy as np
import os
import firebase_admin
from firebase_admin import credentials, firestore

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

# TODO firebase firestore initialization
# Initialize Firebase Admin SDK
# cred = credentials.Certificate("ServiceAccountKey.json")
# default_app = firebase_admin.initialize_app(cred)
# db = firestore.client()
#
# parking_ref = db.collection(u'spotpark') #same with android syntax for CRUD
# docs = parking_ref.get()
#
# for doc in docs:
#     print(u'{} => {}'.format(doc.id, doc.to_dict()))

cap = cv2.VideoCapture(0)
kernel = np.ones((3, 3), np.uint8)

min_width = 200
max_width = 500
threshold_detection = 4000
img_counter = 0

# TODO car plate number detection
while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # For canny detection, translate the frame to grayscale
    # then detect the status of occupancy
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = auto_canny(blurred)

    # For finding the rectangle, only want the rect color
    lower_gray = np.array([0, 0, 0])
    upper_gray = np.array([179, 255, 154])
    mask = cv2.inRange(hsv, lower_gray, upper_gray)

    # Do Morphological Transformations
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # 6th parameter = the bigger the number is, the more brighter
    # TODO CHANGE VALUE
    mask = cv2.adaptiveThreshold(mask, 255, cv2.ADAPTIVE_THRESH_MEAN_C
                                 , cv2.THRESH_BINARY, 15, 12)

    # find contours
    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    hull = [cv2.convexHull(c) for c in contours]

    # sort the contours
    hull.sort(key=lambda x: cv2.boundingRect(x)[0])
    number_box = 1

    for contour in hull:
        # For debugging purpose
        # cv2.drawContours(frame, contour, -1, (0, 255, 0), 3)
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

        # if it is square
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(contour)

            # TODO change the width value depending on camera position
            if w > min_width and w < max_width:
                # Debugging for the rect width
                # print(w)
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # extract the Region of Interest of canny
                roi = canny[y: y + h, x: x + w]
                cv2.putText(frame, str(number_box), cv2.boundingRect(contour[0])[:2],
                            cv2.FONT_HERSHEY_SIMPLEX, 1, [0,0,255], 3)

                # calculate how many non black pixel in the ROI
                roi_value = cv2.countNonZero(roi)

                # For debugging
                # print how many of non black pixel and show the ROI
                # print(park1)
                # cv2.imshow('roi', roi)

                # TODO change the value of threshold_detection accordingly
                # TODO update firestore value occupancy
                if roi_value > threshold_detection:

                    # After Detect taken space
                    # Delay 1 minutes, demo purpose delay 5 sec

                    print(str(number_box) + " got parked car")
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                    cv2.imwrite("parking_car.jpg", frame)
                    # TODO check detected OCR. Must minimum 4 characters
                    # detect_text("parking_car.jpg")
                    # Send to the corresponding parking space db number (if number == 1)
                    # set Available = false


                else:
                    # If no more taken, same delay
                    print(str(number_box) + " no car")
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # delete plate number in corresponding parking space db number
                    # set Available = true

                number_box += 1

    cv2.imshow('Final Outcome', frame)
    cv2.imshow('canny', canny)
    cv2.imshow('Mask', mask)
    cv2.imshow('hsv', hsv)
    cv2.imshow('gray', gray)
    cv2.imshow('blurred', blurred)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
