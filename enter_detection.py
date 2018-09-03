from utility import *
import pymysql
from datetime import datetime

# For canny detection, translate the frame to grayscale and to canny edge detection
# then detect the status of occupancy
car_threshold_value = 1000
cap = cv2.VideoCapture(0)
temp_car_plate_number = ""

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = auto_canny(blurred)
    canny_value = cv2.countNonZero(canny)
    # print(canny_value)

    # For debugging purpose. Checks onto cloud vision api and database
    # spacebar to take photo
    # k = cv2.waitKey(1)
    # if k%256 == 32:
    #     time.sleep(3)
    #     cv2.imwrite("enter_car.jpg", frame)
    #     car_plate_number = detect_text("enter_car.jpg")
    #
    #     if temp_car_plate_number != car_plate_number:
    #         print("Entry Car Plate Number : ", car_plate_number)
    #
    #         if car_plate_number is not None:
    #             conn = pymysql.connect(host=host, user=user, password=pw, db=db)
    #             cursor = conn.cursor()
    #             sql = "SELECT UID FROM car_plate_numbers WHERE plate_number = (%s)"
    #             cursor.execute(sql, car_plate_number)
    #             print("Found records : ", cursor.rowcount)
    #
    #             # check got matching result or not in car_plate_numbers (check user registered or not in app)
    #             if cursor.rowcount is not 0:
    #                 print("Open Barrier")
    #                 UID = cursor.fetchone()
    #                 print("UID: ", UID[0])
    #                 print("Plate Number: ", car_plate_number)
    #                 print("Start Time: ", datetime.time(datetime.now().replace(microsecond=0)).isoformat())
    #                 print("Date: ", f'{datetime.now():%d-%m-%Y}')
    #
    #                 insert_sql = "INSERT INTO parking_records (UID, start_time, plate_number, date) VALUES (%s, %s, %s, %s)"
    #                 cursor.execute(insert_sql,
    #                                (UID[0]
    #                                 , datetime.time(datetime.now().replace(microsecond=0)).isoformat()
    #                                 , car_plate_number
    #                                 , f'{datetime.now():%d-%m-%Y}'))
    #                 conn.commit()
    #                 print("Inserted new record")
    #                 print("Close Barrier")
    #                 temp_car_plate_number = car_plate_number

    # Check got car enter or not
    if canny_value > car_threshold_value:
        # print("got enter car")
        time.sleep(3)
        cv2.imwrite("enter_car.jpg", frame)
        car_plate_number = detect_text("enter_car.jpg")
        print("Entry Car Plate Number : " , car_plate_number)

        if car_plate_number is not None:

            # check car plate number is same with previous
            if temp_car_plate_number != car_plate_number:

                conn = pymysql.connect(host=host, user=user, password=pw, db=db)
                cursor = conn.cursor()

                sql = "SELECT UID FROM car_plate_numbers WHERE plate_number = (%s)"
                cursor.execute(sql, car_plate_number)
                # print("Found records : ", cursor.rowcount)

                # check got matching result or not in car_plate_numbers (check user registered or not in app)
                if cursor.rowcount is not 0:
                    print("Open Barrier")
                    UID = cursor.fetchone()
                    # print("UID: ", UID[0])
                    # print("Plate Number: ", car_plate_number)
                    # print("Start Time: ", datetime.time(datetime.now().replace(microsecond=0)).isoformat())
                    # print("Date: ", f'{datetime.now():%d-%m-%Y}')

                    insert_sql = "INSERT INTO parking_records (UID, start_time, plate_number, date) VALUES (%s, %s, %s, %s)"
                    cursor.execute(insert_sql,
                                   (UID[0]
                                    , datetime.time(datetime.now().replace(microsecond=0)).isoformat()
                                    , car_plate_number
                                    , f'{datetime.now():%d-%m-%Y}'))
                    conn.commit()
                    print("Inserted new record")
                    print("Close Barrier")
                    temp_car_plate_number = car_plate_number

    cv2.imshow('Final Outcome', frame)
    cv2.imshow('canny', canny)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()




