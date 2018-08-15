import cv2

from skimage import data, img_as_float
from skimage.measure import compare_ssim

cap = cv2.VideoCapture(1)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))

contrast = cv2.imread('contrast.jpg', cv2.IMREAD_COLOR)
contrast = cv2.resize(contrast, (700, 700))  #resize the image
grayscaled_contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)

#contrast threshold
retval_contrast, otsu_threshold_contrast = cv2.threshold(grayscaled_contrast, 125, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
dilation_contrast = cv2.dilate(otsu_threshold_contrast,kernel,iterations = 1)
im2_contrast, contours_contrast, hierarchy_contrast = cv2.findContours(dilation_contrast, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
hull_contrast = [cv2.convexHull(c) for c in contours_contrast]
sorted_rect_contrast = sorted(hull_contrast, key=lambda hull_contrast: cv2.boundingRect(hull_contrast)[0])


#Conrast operation
largest_contour_area = 0
pic_num = 1
for i, cnt in enumerate(hull_contrast):
    area = cv2.contourArea(cnt)
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)

    if len(approx) == 4:
        if area > largest_contour_area:
            largest_contour_area = area
        else:
            if(area > 2000):
                x, y, w, h = cv2.boundingRect(cnt)
                
                # write the contrast Region of Image into disk
                roi = contrast[y:y+h, x:x+w]
                roi_resize = cv2.resize(roi, (500,220), interpolation = cv2.INTER_LINEAR)
                cv2.imwrite("contrast_roi"+str(pic_num)+".jpg", roi_resize)
                pic_num += 1
                
pic_num = 1
while True:
    ret, frame = cap.read()
    grayscaled = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    retval, otsu_threshold = cv2.threshold(grayscaled, 125, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    dilation = cv2.dilate(otsu_threshold,kernel,iterations = 1)
    im2, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hull = [cv2.convexHull(c) for c in contours]
    sorted_rect_original = sorted(hull, key=lambda hull: cv2.boundingRect(hull)[0])

##    pic_num = 1
    number_box = 1

    for cnt in hull:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        
        if len(approx) == 4: #if it is square or rectangle
            x, y, w, h = cv2.boundingRect(cnt)
            # print(w)
            if w > 200 and w < 400:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, str(number_box), cv2.boundingRect(cnt[0])[:2], cv2.FONT_HERSHEY_SIMPLEX, 1, [0,0,255], 3)

                # Extract the ROI of the bounding rect of original and contrast
                roi = frame[y:y+h, x:x+w]
                roi_resize = cv2.resize(roi, (500,220), interpolation = cv2.INTER_LINEAR)
                contrast_image = cv2.imread("contrast_roi1.jpg") #problem

                # grayscale the ROI before calculate
                original_image = cv2.cvtColor(roi_resize, cv2.COLOR_BGR2GRAY)
                contrast_image = cv2.cvtColor(contrast_image, cv2.COLOR_BGR2GRAY)

                #calculate the score
                score = compare_ssim(original_image, contrast_image)
                print("Parking number " + str(number_box) + " SSIM: %f" %score)

                if(score < 0.50):
                    print("Got car")
                    # cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                else:
                    print("no car")
                    # cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

                pic_num += 1
                if(pic_num > 3):
                    pic_num = 1
                number_box += 1
                
            #cv2.drawContours(frame,[cnt],0,(0,255,0),3)

    # cv2.imshow('grayscaled', grayscaled)
    cv2.imshow('Otsu threshold', otsu_threshold)
    # cv2.imshow('dilation', dilation)
    # cv2.imshow('contrast', contrast)
    cv2.imshow('Final Outcome', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()

