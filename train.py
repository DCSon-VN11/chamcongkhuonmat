# -*- coding: utf-8 -*-
"""
Created on Tue 12 March 2019

@author: Jaya Sharma
"""

import csv
import datetime
import sqlite3
import time
import tkinter.messagebox as msgbox
from tempfile import NamedTemporaryFile

import cv2
import numpy as np
import os
import pandas as pd
from PIL import Image


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


# set text style
fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 1
fontcolor = (0, 255, 0)
fontcolor1 = (0, 0, 255)


def insertOrUpdate(id, name, age, gender, cr):
    conn = sqlite3.connect("FaceBaseNew.db")
    cursor = conn.execute('SELECT * FROM People WHERE ID=' + str(id))
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
        break

    if isRecordExist == 1:
        cmd = "UPDATE people SET Name=' " + str(name) + " ',Age=' " + str(age) + " ',Gender=' " + str(
            gender) + " ',CR=' " + str(cr) + " ' WHERE ID=" + str(id)
    else:
        cmd = "INSERT INTO people(ID,Name,Age,Gender,CR) Values(" + str(id) + ",' " + str(name) + " ',' " + str(
            age) + " ',' " + str(gender) + " ',' " + str(cr) + " ' )"
    conn.execute(cmd)
    conn.commit()
    conn.close()


# Take Images
def TakeImages(Id, name, age, gender, cr):
    if (is_number(Id) and name.isalpha()):
        insertOrUpdate(Id, name, age, gender, cr)
        cam = cv2.VideoCapture(0)
        cam.set(3, 1920)
        cam.set(4, 1080)
        # load model haarcascade
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            # chuyển về ảnh xám
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # nhận diện khuôn mặt
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                # vẽ 1 đường bao quanh khuôn mặt
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # số mẫu tăng dần
                sampleNum = sampleNum + 1
                # lưu khuôn mặt đã chụp vào thư mục tập dữ liệu TrainingImage
                cv2.imwrite("TrainingImage\ " + name + "." + Id + '.' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                cv2.putText(img, str(sampleNum), (x, y + h + 30), fontface, fontscale, fontcolor, 2)
                # hiển thị khung
                cv2.imshow('frame', img)

            # đợi trong 100 mili giây
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # phá vỡ nếu số lượng mẫu nhiều hơn 100
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Ảnh của bạn đã được lưu với ID : " + Id + " Name : " + name
    else:
        if (is_number(Id) == False):
            res = "Nhập ID là số"
            msgbox.showerror('Error', res)
        if (name.isalpha() == False):
            res = "Nhập tên theo thứ tự bảng chữ cái"
            msgbox.showerror('Error', res)


# Train Images
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    # Lấy các khuôn mặt và ID từ thư mục TrainingImage
    faces, Id = getImagesAndLabels("TrainingImage")
    # Train model để trích xuất đặc trưng các khuôn mặt và gán với từng nahan viên
    recognizer.train(faces, np.array(Id))
    # luu Model
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Ảnh của bạn đã được train thành công"  # +",".join(str(f) for f in Id)
    msgbox.showinfo('Success', res)


def getImagesAndLabels(path):
    # lấy đường dẫn của tất cả các tệp trong thư mục
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # print(imagePaths)

    # tạo danh sách khuôn mặt trống
    faces = []
    # tạo danh sách ID trống
    Ids = []
    # bây giờ lặp qua tất cả các đường dẫn hình ảnh và tải các Id và hình ảnh
    for imagePath in imagePaths:
        # tải hình ảnh và chuyển đổi nó sang thang màu xám
        pilImage = Image.open(imagePath).convert('L')
        # chuyển đổi hình ảnh PIL thành mảng numpy
        imageNp = np.array(pilImage, 'uint8')
        # cv2.imshow('training', imageNp)
        # cv2.waitKey(10)
        # lấy Id từ hình ảnh
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # trích xuất khuôn mặt từ mẫu hình ảnh đào tạo
        faces.append(imageNp)
        Ids.append(Id)

    return faces, Ids


def getProfile(id):
    conn = sqlite3.connect("FaceBaseNew.db")
    cursor = conn.execute("SELECT * FROM People WHERE ID=" + str(id))
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile


# Track Images
def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainingImageLabel\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);
    cam = cv2.VideoCapture(0)
    cam.set(3, 1920)
    cam.set(4, 1080)
    font = cv2.FONT_HERSHEY_SIMPLEX
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")
    fileName = "Attendance\Attendance_" + date + ".csv"
    fileName_statistic = "AttendanceStatistic\AttendanceStatistic_" + date + ".csv"
    col_names = ['Id', 'Name', 'Date', 'Time', 'Status']
    col_name_statistic = ['Id', 'Name', 'Date', 'Time In', 'Time Out', 'Total time']
    attendance = pd.DataFrame(columns=col_names)
    attendance_statistic = pd.DataFrame(columns=col_name_statistic)
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        # Phát hiện các khuôn mặt trong ảnh camera
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        # Lặp qua các khuôn mặt nhận được để hiện thông tin
        for (x, y, w, h) in faces:
            # Vẽ hình chữ nhật quanh mặt
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            # Nhận diện khuôn mặt, trả ra 2 tham số id: mã nhân viên và conf (dộ sai khác)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            profile = None
            arrId = []
            if (conf < 50):
                profile = getProfile(Id)
                # Hiển thị thông tin tên người hoặc Unknown nếu không tìm thấy
            if (profile != None):
                if (os.path.isfile(fileName)):
                    with open(fileName) as f:
                        reader = csv.reader(f)
                        for row in reader:
                            if (row[0] == str(Id)):
                                arrId.append(Id)
                if (arrId.count(Id) == 0):
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa = profile[1]
                    status = 'In'
                    attendance.loc[len(attendance)] = [Id, aa, date, timeStamp, status]
                    attendance_statistic.loc[len(attendance)] = [Id, aa, date, timeStamp, '0', '0']
                if (arrId.count(Id) == 1):
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa = profile[1]
                    status = 'Out'
                    attendance.loc[len(attendance)] = [Id, aa, date, timeStamp, status]
                    df = pd.read_csv(fileName_statistic)
                    with open(fileName_statistic) as f:
                        reader = csv.reader(f)
                        index = df.index[df['Id'] == Id].tolist()
                        for row in reader:
                            if (row[0] == str(Id)):
                                df.loc[index[0], 'Time Out'] = timeStamp
                                df.loc[index[0], 'Total time'] = datetime.datetime.strptime(timeStamp,
                                                                                            '%H:%M:%S') - datetime.datetime.strptime(
                                    row[3], '%H:%M:%S')
                                df.to_csv(fileName_statistic, index=False)

                cv2.putText(im, "Id: " + str(profile[0]), (x, y + h + 30), fontface, fontscale, fontcolor, 2)
                cv2.putText(im, "Name: " + str(profile[1]), (x, y + h + 60), fontface, fontscale, fontcolor, 2)
                cv2.putText(im, "Age: " + str(profile[2]), (x, y + h + 90), fontface, fontscale, fontcolor, 2)

            else:
                cv2.putText(im, "Name: Unknown", (x, y + h + 30), fontface, fontscale, fontcolor1, 2)
        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        attendance_statistic = attendance_statistic.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('im', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    if (os.path.isfile(fileName)):
        attendance.to_csv(fileName, mode='a', index=False, header=False)
    else:
        attendance.to_csv(fileName, mode='a', index=False)

    if (os.path.isfile(fileName_statistic)):
        attendance_statistic.to_csv(fileName_statistic, mode='a', index=False, header=False)
    else:
        attendance_statistic.to_csv(fileName_statistic, mode='a', index=False)

    cam.release()
    cv2.destroyAllWindows()
    # print(attendance)
    res = attendance
    msgbox.showinfo("Message", 'Bạn đã chấm công thành công!')
