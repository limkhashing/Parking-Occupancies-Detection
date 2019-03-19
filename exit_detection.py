from utility import *
import pymysql
from datetime import datetime

car_threshold_value = 1000
cap = cv2.VideoCapture(1)
temp_car_plate_number = ""

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = auto_canny(blurred)
    canny_value = cv2.countNonZero(canny)
    # print(canny_value)

    # For debugging purpose. Checks onto cloud vision api
    # spacebar to take photo
    # k = cv2.waitKey(1)
    # if k%256 == 32:
    #     cv2.imwrite("exit_car.jpg", frame)
    #     car_plate_number = detect_text("exit_car.jpg")
    #     print("Exit Car Plate Number : " , car_plate_number)
    #
    #     # if is not null
    #     if car_plate_number is not None:
    #
    #         # check car plate number is same with previous
    #         if temp_car_plate_number != car_plate_number:
    #
    #             conn = pymysql.connect(host=host, user=user, password=pw, db=db)
    #             cursor = conn.cursor()
    #
    #             select_sql = "SELECT records_ID, start_time FROM parking_records WHERE plate_number = (%s) AND end_time IS NULL"
    #             cursor.execute(select_sql, car_plate_number)
    #             print("Found records : ", cursor.rowcount)
    #
    #             # check got matching result or not in parking_records
    #             # plate_number must match end_time is null
    #             if cursor.rowcount is not 0:
    #                 results = cursor.fetchone()
    #                 records_ID = results[0]
    #                 start_time = results[1]
    #                 end_time = datetime.time(datetime.now().replace(microsecond=0)).isoformat()
    #
    #                 print("records_ID: ", records_ID)
    #                 print("start_time: ", start_time)
    #                 print("end_time: ", end_time)
    #
    #                 # get time interval (duration)
    #                 FMT = '%H:%M:%S'
    #                 duration = datetime.strptime(end_time, FMT) - datetime.strptime(start_time, FMT)
    #                 print("Duration: ", duration)
    #
    #                 # get individual duration. hour minutes seconds
    #                 string_duration = list(map(int, f'{duration}'.split(":")))
    #                 hour = string_duration[0]
    #                 minutes = string_duration[1]
    #                 seconds = string_duration[2]
    #
    #                 # retrieve active(1) parking rates
    #                 rates_sql = "SELECT active, first_hour, following_two_hour, following_fourth_hour FROM parking_rates WHERE active = 1"
    #                 cursor.execute(rates_sql)
    #
    #                 # if got result from query retrieve active parking rates
    #                 if cursor.rowcount is not 0:
    #                     results = cursor.fetchone()
    #                     first_hour = results[1]
    #                     following_two_hour = results[2]
    #                     following_fourth_hour = results[3]
    #
    #                     # calculate parking fees
    #                     parking_fees = 0
    #                     if hour < 1:
    #                         parking_fees = first_hour
    #                     elif hour <= 2:
    #                         parking_fees = first_hour + following_two_hour
    #                     elif hour >= 3:
    #                         parking_fees = first_hour + following_two_hour
    #                         for parking_fees in range(hour):
    #                             parking_fees += following_fourth_hour
    #
    #                     # update the parking record with end_time, duration, and parking_fees
    #                     update_sql = "UPDATE parking_records SET end_time = (%s), duration = (%s), paid_parking_fee = (%s) WHERE records_ID = (%s)"
    #                     cursor.execute(update_sql,
    #                                    (end_time, f'{duration}', parking_fees, records_ID))
    #                     conn.commit()
    #                     print("Updated record")
    #                     print("Open Barrier")
    #                     # TODO Auto pay at mobile app then only update records
    #                     print("Close Barrier")
    #                     temp_car_plate_number = car_plate_number

    # The real detection starts here
    # Check got car exit or not
    if canny_value > car_threshold_value:
        # print("got exit car")
        cv2.imwrite("exit_car.jpg", frame)
        car_plate_number = detect_text("enter_car.jpg")
        print("Exit Car Plate Number : " , car_plate_number)

        # if is not null
        if car_plate_number is not None:

            # check car plate number is same with previous
            if temp_car_plate_number != car_plate_number:

                conn = pymysql.connect(host=host, user=user, password=pw, db=db)
                if conn.open:
                    cursor = conn.cursor()

                    select_sql = "SELECT records_ID, start_time FROM parking_records WHERE plate_number = (%s) AND end_time IS NULL"
                    cursor.execute(select_sql, car_plate_number)
                    print("Found records : ", cursor.rowcount)

                    # check got matching result or not in parking_records
                    # plate_number must match end_time is null
                    if cursor.rowcount is not 0:
                        results = cursor.fetchone()
                        records_ID = results[0]
                        start_time = results[1]
                        end_time = datetime.time(datetime.now().replace(microsecond=0)).isoformat()

                        print("records_ID: ", records_ID)
                        print("start_time: ", start_time)
                        print("end_time: ", end_time)

                        # get time interval (duration)
                        FMT = '%H:%M:%S'
                        duration = datetime.strptime(end_time, FMT) - datetime.strptime(start_time, FMT)
                        print("Duration: ", duration)

                        # get individual duration. hour minutes seconds
                        string_duration = list(map(int, f'{duration}'.split(":")))
                        hour = string_duration[0]
                        minutes = string_duration[1]
                        seconds = string_duration[2]

                        # retrieve active(1) parking rates
                        rates_sql = "SELECT active, first_hour, following_two_hour, following_fourth_hour FROM parking_rates WHERE active = 1"
                        cursor.execute(rates_sql)

                        # if got result from query retrieve active parking rates
                        if cursor.rowcount is not 0:
                            results = cursor.fetchone()
                            first_hour = results[1]
                            following_two_hour = results[2]
                            following_fourth_hour = results[3]

                            # calculate parking fees
                            parking_fees = 0
                            if hour < 1:
                                parking_fees = first_hour
                            elif hour <= 2:
                                parking_fees = first_hour + following_two_hour
                            elif hour >= 3:
                                parking_fees = first_hour + following_two_hour
                                for parking_fees in range(hour):
                                    parking_fees += following_fourth_hour

                            # update the parking record with end_time, duration, and parking_fees
                            update_sql = "UPDATE parking_records SET end_time = (%s), duration = (%s), paid_parking_fee = (%s) WHERE records_ID = (%s)"
                            cursor.execute(update_sql,
                                           (end_time, f'{duration}', parking_fees, records_ID))
                            conn.commit()
                            print("Updated record")
                            print("Open Barrier")
                            # TODO Auto pay at mobile app then only updatre records
                            print("Close Barrier")
                            temp_car_plate_number = car_plate_number
                else:
                    print("Connection with db is not open")

    cv2.imshow('Final Outcome', frame)
    # cv2.imshow('canny', canny)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()




