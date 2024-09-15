import tkinter as tk
import tkinter.font as font

from train import TakeImages
from train import TrainImages


def demo(e1, e2, e3, e4, e5):
    Id = str(e1.get())
    name = str(e2.get())
    age = str(e3.get())
    gender = str(e4.get())
    cr = str(e5.get())
    msg = TakeImages(Id, name, age, gender, cr)


def draw_ui():
    master = tk.Tk()
    width = 600
    height = 400
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    master.geometry("%dx%d+%d+%d" % (width, height, x, y))
    master.title("Thêm mới nhân viên")
    helv24 = font.Font(family='Helvetica', size=16, weight=font.BOLD)
    tk.Label(master, text="ID", font=helv24).place(x=150, y=50, anchor="center")
    tk.Label(master, text="Tên", font=helv24).place(x=150, y=100, anchor="center")
    tk.Label(master, text="Tuổi", font=helv24).place(x=150, y=150, anchor="center")
    tk.Label(master, text="Giới tính", font=helv24).place(x=150, y=200, anchor="center")
    tk.Label(master, text="Vị trí", font=helv24).place(x=150, y=250, anchor="center")

    e1 = tk.Entry(master, width=30)
    e2 = tk.Entry(master, width=30)
    e3 = tk.Entry(master, width=30)
    e4 = tk.Entry(master, width=30)
    e5 = tk.Entry(master, width=30)

    e1.place(x=300, y=50, anchor="center", height=20)
    e2.place(x=300, y=100, anchor="center", height=20)
    e3.place(x=300, y=150, anchor="center", height=20)
    e4.place(x=300, y=200, anchor="center", height=20)
    e5.place(x=300, y=250, anchor="center", height=20)

    tk.Button(master, text="Lấy ảnh", bg="#01a157", fg='white', font=helv24,
              command=lambda: demo(e1, e2, e3, e4, e5)).place(x=200, y=350, anchor="center")
    tk.Button(master, text="Train ảnh", bg="#00c0ef", fg='white', font=helv24, command=TrainImages).place(x=400, y=350,
                                                                                                          anchor="center")
    master.mainloop()
