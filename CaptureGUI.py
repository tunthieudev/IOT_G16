import cv2
import face_recognition
import pickle
import time
from tkinter import *
from datetime import datetime
import csv
import os
import threading

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://iot-n11-faceattendance-default-rtdb.firebaseio.com/",
    'storageBucket': "iot-n11-faceattendance.appspot.com"
})

ref = db.reference("Students")

# data_list = []

# with open("id list.csv", 'r') as csv_file:
#     csv_reader = csv.reader(csv_file)

#     for row in csv_reader:
#         data_list.append(row)


def submit(userid, username, image):
    data = {}

    # id = str(int(data_list[len(data_list)-1][0]) + 1)
    id = userid
    data[id] = {}

    data[id]["name"] = username

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    data[id]["last_attendance_time"] = formatted_datetime

    data[id]["total_attendance"] = 1

    print(data)
    for key, value in data.items():
        ref.child(key).set(value)

    newImagePath = "Images/" + id + ".png"
    cv2.imwrite(newImagePath, image)
    bucket = storage.bucket()
    blob = bucket.blob(newImagePath)
    blob.upload_from_filename(newImagePath)

    # with open("id list.csv", mode='a', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow([id, username])

    print("Encoding Started...")
    img = cv2.imread(newImagePath)
    imgList = []
    studentIds = []
    imgList.append(img)
    studentIds.append(id)

    encodeList = []
    for imageInList in imgList:
        convertedImage = cv2.cvtColor(imageInList, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(convertedImage)[0]
        encodeList.append(encode)

    encodeListWithIds = [encodeList, studentIds]
    print("Encoding Complete")

    file = open("EncodeFile.p", 'wb')
    pickle.dump(encodeListWithIds, file)
    file.close()
    print("File saved")


def capture_square_webcam_image(userid, username):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()

        height, width, _ = frame.shape
        size = min(height, width)
        start_x = (width - size) // 2
        start_y = (height - size) // 2
        square_frame = frame[start_y:start_y+size, start_x:start_x+size]

        display_frame = cv2.resize(square_frame, (500, 500))
        cv2.imshow("Webcam | Space to Save, Esc to Exit", display_frame)

        key = cv2.waitKey(1)
        if key == 27:
            break
        elif key == 32:
            image = cv2.resize(square_frame, (216, 216))
            print("Image captured!")
            submit(userid, username, image)
            break

    cap.release()
    time.sleep(2)
    cv2.destroyAllWindows()