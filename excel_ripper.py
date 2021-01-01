import csv
from os import listdir
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import tkinter as tk
from tkinter import ttk

from tkcalendar import DateEntry


files_here = listdir()

hours = mdates.HourLocator()

epoch_values = []


for test_file in files_here:
    if ".CSV" not in test_file:
        files_here.remove(test_file)
    else:
        with open(str(test_file), newline='') as csvfile:
            data_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in data_reader:
                value = datetime.fromtimestamp(int(row[0]))
                epoch_values.append(value)

epoch_values.sort()


def show_graph(epoch_local=epoch_values):
    epoch_usage = np.arange(10, ((len(epoch_local) + 1) * 10), 10).tolist()

    # Create figure and plot space
    fig, ax = plt.subplots(figsize=(10, 100))

    # Add x-axis and y-axis
    ax.plot(epoch_local,
            epoch_usage,
            color='blue')

    # Set title and labels for axes
    ax.set(xlabel="Date",
           ylabel="Cumlative Usage (W)",
           title="Weekly Power Usage")

    # Rotate tick marks on x-axis
    plt.setp(ax.get_xticklabels(), rotation=45)

    if(len(epoch_local) < 1000):
        ax.xaxis.set_major_locator(hours)

    plt.show()


def pick_specific_day():
    def run_graph():
        local_vales = []
        print(type(cal.get_date()))
        datetime_object = cal.get_date()
        if(datetime_object >= epoch_values[0].date() and datetime_object <= epoch_values[len(epoch_values) - 1].date()):
            print("Showing: " + str(datetime_object))
            for i in epoch_values:
                if(i.date() == datetime_object):
                    local_vales.append(i)
            show_graph(local_vales)
        else:
            print("That date isn't possible, try again!")

    top = tk.Toplevel(root)

    message = "Select a day from, " + \
        str(epoch_values[0].date()) + " to " + \
        str(epoch_values[len(epoch_values)-1].date())

    ttk.Label(top, text=message).pack(padx=10, pady=10)

    cal = DateEntry(top, width=12, background='darkblue',
                    foreground='white', borderwidth=2)
    cal.set_date(epoch_values[0])
    cal.pack(padx=10, pady=10)

    ttk.Button(top, text="Show graph", command=run_graph).pack()


def pick_date_range():

    def run_graph():
        local_vales = []
        datetime_object_start = cal.get_date()
        datetime_object_end = cal_end.get_date()
        if(datetime_object_start >= epoch_values[0].date() and datetime_object_end <= epoch_values[len(epoch_values) - 1].date() and datetime_object_end > datetime_object_start):
            print("Showing: " + str(datetime_object_start) +
                  " too " + str(datetime_object_end))
            for i in epoch_values:
                if(i.date() >= datetime_object_start and i.date() <= datetime_object_end):
                    local_vales.append(i)
            show_graph(local_vales)
        else:
            print("That date range isn't possible, try again!")

    top = tk.Toplevel(root)

    selected_day_start = "Select a start date after " + \
        str(epoch_values[0].date())

    selected_day_end = "Select a end date before " + \
        str(epoch_values[0].date())

    ttk.Label(top, text=selected_day_start).pack(padx=10, pady=10)

    cal = DateEntry(top, width=12, background='darkblue',
                    foreground='white', borderwidth=2)
    cal.set_date(epoch_values[0])
    cal.pack(padx=10, pady=10)

    tk.Label(top, text=selected_day_end).pack(padx=10, pady=10)

    cal_end = DateEntry(top, width=12, background='darkblue',
                        foreground='white', borderwidth=2)
    cal_end.set_date(epoch_values[len(epoch_values) - 1])
    cal_end.pack(padx=10, pady=10)

    ttk.Button(top, text="Show Graph", command=run_graph).pack()


root = tk.Tk()
s = ttk.Style(root)
s.theme_use('clam')

ttk.Button(root, text='Show one day',
           command=pick_specific_day).pack(padx=10, pady=10)
ttk.Button(root, text='Show date range',
           command=pick_date_range).pack(padx=10, pady=10)
ttk.Button(root, text='Show all dates',
           command=show_graph).pack(padx=10, pady=10)

root.mainloop()
