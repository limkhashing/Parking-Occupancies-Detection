import cv2
import numpy as np

cap = cv2.VideoCapture(1)
kernel = np.ones((3, 3), np.uint8)

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    lower_gray = np.array([0, 0, 0])
    upper_gray = np.array([179, 255, 154])
    mask = cv2.inRange(hsv, lower_gray, upper_gray)

    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # 6th parameter = the bigger the number is, the more brighter
    # TODO CHANGE VALUE
    mask = cv2.adaptiveThreshold(mask, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 12)
    # mask = cv2.adaptiveThreshold(mask, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 12)

    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    hull = [cv2.convexHull(c) for c in contours]
    hull.sort(key=lambda x: cv2.boundingRect(x)[0])
    number_box = 1

    for contour in hull:
        # For debugging purpose
        # cv2.drawContours(frame, contour, -1, (0, 255, 0), 3)
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

        # if it is squaure
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(contour)

            # TODO change the width value on different camera position
            if w > 200 and w < 500:
                # Debugging for the rect width
                # print(w)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                roi = gray[y: y + h, x: x + w]
                cv2.putText(frame, str(number_box), cv2.boundingRect(contour[0])[:2], cv2.FONT_HERSHEY_SIMPLEX, 1, [0,0,255], 3)

                park1 = cv2.countNonZero(roi)
                # print how many of non black pixel. For debugging
                print(park1)
                # show the rectangle only
                cv2.imshow('roi', roi)

                # if there is many white pixel
                # TODO chagne the value of threshold accordingly
                # if park1 < 75000:
                #     print(str(number_box) + " got car")
                #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                # else:
                #     print(str(number_box) + " no car")
                #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                number_box += 1

    cv2.imshow('Final Outcome', frame)
    cv2.imshow('Mask', mask)
    if cv2.waitKey(1000) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
