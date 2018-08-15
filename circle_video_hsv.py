import cv2
import numpy as np

def nothing(x):
    pass

def get_contour_precedence(contour, cols):
    tolerance_factor = 10
    origin = cv2.boundingRect(contour)
    return ((origin[1] // tolerance_factor) * tolerance_factor) * cols + origin[0]


cap = cv2.VideoCapture(1)

# cv2.namedWindow("Trackbars")
# cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
# cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
# cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
# cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
# cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
# cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

kernel = np.ones((3, 3), np.uint8)

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    # l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    # l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    # u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    # u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    # u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    # l_h l_s l_v = 0 0 0
    # u_h u_s u_v = 179 255 154

    lower_gray = np.array([0, 0, 0])
    upper_gray = np.array([179, 255, 154])
    mask = cv2.inRange(hsv, lower_gray, upper_gray)
    mask = cv2.erode(mask, kernel, iterations=6)
    mask = cv2.dilate(mask, kernel, iterations=3)
    closing = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours.sort(key=lambda x: cv2.boundingRect(x)[0])

    for contour in contours:
        # For debugging purpose
        # cv2.drawContours(frame, contour, -1, (0, 255, 0), 3)
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

        # (Cx, Cy), Cr = cv2.minEnclosingCircle(contour)
        # center = (int(Cx), int(Cy))
        # Cr = int(Cr)
        # # print(Cr)
        # # check radius
        # if Cr <= 20:
        #     cv2.circle(frame, center, Cr, (0, 255, 0), 2)

        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(contour)
            if w < 300:
                roi = frame[y: y + h, x: x + w]
                # cv2.drawContours(frame, contour, -3, (0, 255, 0), 3)

                hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                lower_gray_roi = np.array([0, 0, 0])
                upper_gray_roi = np.array([179, 255, 154])
                mask_roi = cv2.inRange(hsv_roi, lower_gray_roi, upper_gray_roi)
                mask_roi = cv2.erode(mask_roi, kernel, iterations=6)
                mask_roi = cv2.dilate(mask_roi, kernel, iterations=3)
                closing_roi = cv2.morphologyEx(mask_roi, cv2.MORPH_CLOSE, kernel)

                got_circle = False

                _, contours_roi, _ = cv2.findContours(mask_roi, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                contours_roi.sort(key=lambda x: cv2.boundingRect(x)[0])
                for contour_roi in contours_roi:
                    (Cx, Cy), Cr = cv2.minEnclosingCircle(contour_roi)
                    center = (int(Cx), int(Cy))
                    Cr = int(Cr)
                    cv2.circle(frame, center, Cr, (0, 255, 0), 2)
                    
##                    if Cr <= 40:
##                        cv2.circle(roi, center, Cr, (0, 255, 0), 2)
##                        got_circle = True

##                    if got_circle:
##                        print("no car")
##                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
##                    if got_circle is False:
##                        print("got car. slot taken")
##                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)


            # TODO ERROR NUMBER BOX
            # cv2.putText(frame, "1", cv2.boundingRect(contour[0])[:2], cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 0, 255], 3)

    # cv2.imshow('otsu_threshold', otsu_threshold)
    # cv2.imshow('dilation', dilation)
    cv2.imshow('Final Outcome', frame)
    cv2.imshow('Mask', mask)
    if cv2.waitKey(1000) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

