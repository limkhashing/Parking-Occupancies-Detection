# PythonSpotPark

This project is used conjunction with mobile application [SpotPark](https://github.com/kslim888/SpotPark) for implement an Indoor Parking System
This repo will install into CCTV cameras for detecting vacant parking slot and also act as a surveillanc in the indoor parking area.
It utilize OpenCV library and Google Cloud Vision API in helping detect parking spaces and extract car plat numbers
The car plate number will be stored in MySQL database.

### Outlines
* utility.py -- Consist of reuse code in other py file
* google_vision_api.py -- Consist of vision_text_detection (OCR) function
* enter_detection.py -- Responsible for detecting cars at entry gate
* exit_detection.py -- Responsible for detecting cars at exit gate
* final_detection.py -- Responsible for detecting cars at parking spaces, and determine the vacancy of it

### Requirements
* CCTV Cameras 
* A sample parking slots, which can draw on a piece of paper

## Built With
* [PyCharm](https://www.jetbrains.com/pycharm/) - The IDE used
* Python programming language

## Authors
* **Lim Kha Shing** - [kslim888](https://github.com/kslim888)
