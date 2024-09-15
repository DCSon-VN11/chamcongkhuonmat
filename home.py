import tkinter as tk
import tkinter.font as font
from tkinter import *

from PIL import ImageTk, Image

from add_new import draw_ui
from attendance import attendance
from attendance_statistic import attendance_statistic
from train import TrackImages


# UI
def open_add_new():
    draw_ui()


window = tk.Tk()
window.title("Chương trình chấm công")
width = 1000
height = 600
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
window.geometry("%dx%d+%d+%d" % (width, height, x, y))
window.resizable(0, 0)
window.configure(background='#f9f9f9')

helv36 = font.Font(family='Helvetica', size=36, weight=font.BOLD)
helv24 = font.Font(family='Helvetica', size=20, weight=font.BOLD)

# logo
img = ImageTk.PhotoImage(Image.open("logo.jpg"))
display = Canvas(window, bg="black", height=50, width=140, bd=0, highlightthickness=0)
display.create_image(0, 0, image=img, anchor=NW, tags="IMG")
display.grid(row=0, column=0, sticky='news', padx=20)

# title
title = tk.Label(window, text="Chương trình chấm công", bg="#f9f9f9", font=helv36)
title.grid(row=0, column=1, columnspan=3, sticky='news')

# button1
mark_attendance = tk.Button(window, text="Chấm công", bg="#00c0ef", font=helv24, command=TrackImages)
mark_attendance.grid(row=1, column=0, columnspan=2, sticky='news', padx=(20, 10), pady=(20, 10))

# button2
check_attendance = tk.Button(window, text="Thống kê chấm công", bg="#f39c11", font=helv24, command=attendance_statistic)
check_attendance.grid(row=1, column=2, columnspan=2, sticky='news', padx=(10, 20), pady=(20, 10))

# button3
add_new_student = tk.Button(window, text="Thêm mới nhân viên", bg="#01a157", font=helv24, command=open_add_new)
add_new_student.grid(row=2, column=0, columnspan=2, sticky='news', padx=(20, 10), pady=(10, 20))

# button4
search_student = tk.Button(window, text="Kiểm tra chấm công", bg="#d84a38", command=attendance, font=helv24)
search_student.grid(row=2, column=2, columnspan=2, sticky='news', padx=(10, 20), pady=(10, 20))

Grid.rowconfigure(window, 0, weight=1)

for x in range(3):
    Grid.rowconfigure(window, x, weight=1)

for y in range(4):
    Grid.columnconfigure(window, y, weight=1)

window.mainloop()
