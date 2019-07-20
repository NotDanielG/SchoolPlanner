from tkinter import *
import calendar
import pickle


def option_changed(*args):
    range = calendar.monthrange(int(selectedYear.get()), int(monthChoice[selectedMonth.get()]))
    print(range)
    cells = args[0]
    counter = range[0] + 1
    if counter >= 7:
        counter = 0
    j = 0
    start = False
    for cell in cells:
        for child in cell.winfo_children():
            child.destroy()
        if j == counter and not start:
            start = True
            j = 1
        if start and j <= range[1]:
            label = Label(cell, text=str(j))
            label.place(x=0, y=0)
        j += 1


def one(event):
    print("One Click")


def two(event):
    print("Two Click")


if __name__ == '__main__':
    root = Tk()
    root.geometry("1280x720")
    root.resizable(False, False)
    root.configure()

    dict = {}
    dict_day = {1: "Task One"}
    dict_month = {"January": dict_day}
    dict[2000] = dict_month

    pickle_out = open("test.pickle", "wb")
    pickle.dump(dict, pickle_out)
    pickle_out.close()

    pickle_in = open("test.pickle", "rb")
    entry = pickle.load(pickle_in)

    leftPane = PanedWindow(background="black", height=720, width=480)
    calendarPane = PanedWindow(background="gray", width=800)
    leftPane.pack(fill=BOTH, side=LEFT)
    calendarPane.pack(fill=BOTH, side=RIGHT)

    calendarFrame = Frame(calendarPane, bg="red", width=770, height=570)
    calendarFrame.place(x=15, y=100)

    calX = 15
    calY = 75

    dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    for name in dayNames:
        test = Frame(calendarPane, bg="red", width=110, height=25)
        test.place(x=calX, y=calY)
        label = Label(test, text=name)
        label.place(x=60, y=0)
        label.place(x=110-label.winfo_reqwidth())
        calX += 110

    count = 34
    calX = 0
    calY = 0
    dayCells = list()
    while count >= 0:
        # test = Frame(calendarFrame, bg="blue", borderwidth=1, width=110, height=114)
        test = (calendarFrame, bg="blue", borderwidth=1, width=110, height=114)
        label = Label(test, text=str(35-count))
        label.place(x=0, y=0)
        test.bind("<Double-1>", two)
        test.place(x=calX, y=calY)
        dayCells.append(test)
        calX += 110
        if count % 7 == 0 and count != 35:
            calY += 114
            calX = 0
        count += -1

    monthChoice = {}
    count = 1
    for month in calendar.month_name:
        if month != "":
            monthChoice[month] = count
            count += 1
    selectedMonth = StringVar()
    selectedMonth.set(list(monthChoice.keys())[0])
    selectedMonth.trace("w", lambda name, index, mode, dayCells=dayCells: option_changed(dayCells))

    monthMenu = OptionMenu(calendarPane, selectedMonth, *monthChoice)
    monthMenu.place(x=315, y=10)
    monthMenu.config(width=10, indicator=0)

    yearList = range(2019,2030)
    yearChoice = {}
    for year in yearList:
        yearChoice[year] = year
    selectedYear = StringVar()
    selectedYear.set(list(yearChoice.keys())[0])
    selectedYear.trace("w", lambda name, index, mode, dayCells=dayCells: option_changed(dayCells))

    yearMenu = OptionMenu(calendarPane, selectedYear, *yearChoice)
    yearMenu.place(x=455, y=10)
    yearMenu.config(width=10, indicator=0)

    # monthrange 0 = monday
    dayList = range(1, calendar.monthrange(int(selectedYear.get()), int(monthChoice[selectedMonth.get()]))[1])
    monRange = calendar.monthrange(int(selectedYear.get()), int(monthChoice[selectedMonth.get()]))

    count = monRange[0] + 1
    if count >= 8:
        count = 0
    i = 0
    start = False
    for cell in dayCells:
        for child in cell.winfo_children():
            child.destroy()
        if i == count and not start:
            start = True
            i = 1
        if start and i <= monRange[1]:
            label = Label(cell, text=str(i))
            label.place(x=0, y=0)
        i += 1

    mainloop()
