import urllib.request
import cv2
import numpy as np

#TODO detect car from IP camera
url = 'rtsp://192.168.0.132:554/onvif1'

while True:
    imgResp = urllib.request.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)

    # all the opencv processing is done here
    cv2.imshow('test',img)
    if ord('q')==cv2.waitKey(10):
        exit(0)



'''   
import numpy as np
import cv2

cap = cv2.VideoCapture('rtsp://192.168.0.132:554/onvif1')
#cap = cv2.VideoCapture('video1.avi')
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('frame', 900,600)

while(True):
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
'''
