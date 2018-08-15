import cv2

cap = cv2.VideoCapture(1)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
     
    #grayscale the frame
    grayscaled = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #original threshold
    retval, otsu_threshold = cv2.threshold(grayscaled, 125, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    dilation = cv2.dilate(otsu_threshold, kernel, iterations = 1)
    im2, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hull = [cv2.convexHull(c) for c in contours]

    # Sort the contours
    sorted_rect_original = sorted(hull, key=lambda hull: cv2.boundingRect(hull)[0])

    number_box = 1

    for cnt in hull:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)

        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(cnt)
            print(w)
            if 100 < w < 500:
                roi = frame[y:y+h, x:x+w]
                cv2.imshow('roi', roi)
                
                got_circle = False

                grayscaled_circle = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                retval, otsu_threshold_circle = cv2.threshold(grayscaled_circle, 125, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                dilation_circle = cv2.dilate(otsu_threshold_circle, kernel, iterations = 1)
                im2, contours_circle, hierarchy = cv2.findContours(dilation_circle, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                hull_circle = [cv2.convexHull(c) for c in contours_circle]
                sorted_contour_circle = sorted(hull_circle, key=lambda hull_circle: cv2.boundingRect(hull_circle)[0])
                for cnt_roi in hull_circle:
                    (Cx,Cy), Cr = cv2.minEnclosingCircle(cnt_roi)
                    center = (int(Cx),int(Cy))
                    Cr = int(Cr)
                    cv2.circle(roi, center, Cr, (0,255,0),2)
                    
##                    approx_circle = cv2.approxPolyDP(cnt_roi,0.01*cv2.arcLength(cnt_roi,True),True)
##                    if Cr >= 6 and Cr <= 15:
##                        cv2.circle(roi, center, Cr, (0,255,0),2)
##                        got_circle = True

##                if got_circle:
##                    print("no car.")
##                    cv2.rectangle(frame, (x,y),(x+w,y+h), (0, 255, 0), 2)
##                else:
##                    print("got car. slot taken")
##                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255), 2)

                # TODO ERROR NUMBER BOX
                # cv2.putText(frame, str(number_box), cv2.boundingRect(cnt[0])[:2], cv2.FONT_HERSHEY_SIMPLEX, 1, [0,0,255], 3)

                number_box += 1
    cv2.imshow('otsu_threshold', otsu_threshold)
    cv2.imshow('dilation', dilation)
    cv2.imshow('Final Outcome', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()

