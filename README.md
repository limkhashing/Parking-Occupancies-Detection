# PythonSpotPark

This project is used conjunction with mobile application [SpotPark](https://github.com/kslim888/SpotPark) for implement an Indoor Parking System
This repo will install into CCTV cameras for detecting vacant parking slot and also act as a surveillanc in the indoor parking area.
It utilize OpenCV library and Google Cloud Vision API in helping detect parking spaces and extract car plat numbers
The car plate number will be stored in MySQL database.

For a demo on how car plate number is detected, please see the YouTube video 
https://youtu.be/L6TEvo5vyVs


### Outlines
* utility.py -- Consist of reuse code in other py file
* google_vision_api.py -- Consist of vision_text_detection (OCR) function
* enter_detection.py -- Responsible for detecting cars at entry gate
* exit_detection.py -- Responsible for detecting cars at exit gate
* final_detection.py -- Responsible for detecting cars at parking spaces, and determine the vacancy of it

### Requirements
* CCTV Cameras 
* A sample parking slots, which can draw on a piece of paper

#### Detecting vehicle at entrance
![image](https://user-images.githubusercontent.com/30791939/54375819-ba020000-46bc-11e9-8af1-410d0aea03f4.png)

#### Detecting Car Plate Number
![image](https://user-images.githubusercontent.com/30791939/54375894-e1f16380-46bc-11e9-929f-6a254201b374.png)

#### Occupancies Dection
![image](https://user-images.githubusercontent.com/30791939/54376034-1d8c2d80-46bd-11e9-96bf-126dfa24d5fa.png)

## Built With
* [PyCharm](https://www.jetbrains.com/pycharm/) - The IDE used
* Python programming language

## Authors
* [**Lim Kha Shing**](https://www.linkedin.com/in/lim-kha-shing-836a24120/)
