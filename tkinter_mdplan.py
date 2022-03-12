from tkinter import *
from tkcalendar import *


def open_plan_window():
    global plan_window
    plan_window = Toplevel()
    plan_window.geometry("200x300")
    plan_window.title("Erstelle Plan")
    Label(plan_window, text="Not implemented yet").pack()
    root.iconify()


def open_holiday_window():
    global holiday_window
    holiday_window = Toplevel()
    holiday_window.geometry("200x300")
    holiday_window.title("Urlaub Eintragen")
    Label(holiday_window, text="Not implemented yet").pack()
    root.iconify()


def open_churchserver_window():
    global churchserver_window
    churchserver_window = Toplevel()
    churchserver_window.geometry("200x300")
    churchserver_window.title("Verwalte Messdiener")
    Label(churchserver_window, text="Not implemented yet").pack()
    root.iconify()


root = Tk()
root.title("Messdienerplan_Auswahl")
root.geometry("500x500")


# creates  buttons to open different parts of the application
button_manage_churchservers = Button(root, text="Manage Messdiener", command=open_churchserver_window, height= 3).pack()
button_manage_holidays = Button(root, text="Urlaub", command=open_holiday_window, height= 3).pack()
button_create_plan = Button(root, text="Erstelle Plan", command=open_plan_window, height= 3).pack()


root.mainloop()
