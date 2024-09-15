# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 18:10:17 2022

@author: Admin
"""

import csv
import datetime
import time
import tkinter.ttk as ttk
from tkinter import *


def attendance_statistic():
    root = Tk()
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    root.title("Thống kế chấm công ngày " + date)
    width = 600
    height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(None, None)
    TableMargin = Frame(root, width=500)
    TableMargin.pack(side=TOP)
    scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    tree = ttk.Treeview(TableMargin, columns=("Id", "Name", "Date", "Time In", "Time Out", 'Total Time'), height=400,
                        selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Id', text="Id", anchor=W)
    tree.heading('Name', text="Name", anchor=W)
    tree.heading('Date', text="Date", anchor=W)
    tree.heading('Time In', text="Check in", anchor=W)
    tree.heading('Time Out', text="Check out", anchor=W)
    tree.heading('Total Time', text="Total Time", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=50)
    tree.column('#2', stretch=NO, minwidth=0, width=100)
    tree.column('#3', stretch=NO, minwidth=0, width=100)
    tree.column('#4', stretch=NO, minwidth=0, width=100)
    tree.column('#5', stretch=NO, minwidth=0, width=100)
    tree.pack()

    fileName = "AttendanceStatistic\\AttendanceStatistic_" + date + ".csv"
    with open(fileName) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            Id = row['Id']
            Name = row['Name']
            Date = row['Date']
            TimeIn = row['Time In']
            Timeout = row['Time Out']
            Total = row['Total time']
            tree.insert("", 0, values=(Id, Name, Date, TimeIn, Timeout, Total))

    root.mainloop()
