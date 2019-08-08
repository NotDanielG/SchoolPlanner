from tkinter import *
import calendar
import pickle
from tkinter_subclass import *

try:
    pickle_in = open("test.pickle", "rb")
    entry = pickle.load(pickle_in)
    print(entry)
    dictionary_calendar = entry
except EOFError:
    dictionary_calendar = dict()


def option_changed(*args):
    # FORMAT CALENDAR ON MONTH OR YEAR CHANGE
    range = calendar.monthrange(int(selectedYear.get()), int(monthChoice[selectedMonth.get()]))
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
            label = Label(cell, text=str(j), bg="white")
            cell.set_day(j)
            # label.place(x=0, y=0)
            label.pack(side=LEFT, anchor=N)
            if selectedYear.get() in dictionary_calendar and selectedMonth.get() in dictionary_calendar[
                    selectedYear.get()] and i in dictionary_calendar[selectedYear.get()][selectedMonth.get()]:
                for title in dictionary_calendar[selectedYear.get()][selectedMonth.get()][i]:
                    task_title = Label(cell, text=title)
                    task_title.pack(anchor=W)
        if not start or j > range[1]:
            cell.set_day(0)
        cell.bind("<Double-1>", lambda event, day_number=cell.get_day(): double_click(event, day_number))
        cell.bind("<Button-1>", lambda event, day_number=cell.get_day(): one_click(event, day_number))
        j += 1


def one_click(event, day_number):
    # Use day number, month and year to find tasks and respective description
    global dictionary_calendar
    d = ""
    t = ""
    y = 5
    if selectedYear.get() in dictionary_calendar and selectedMonth.get() in dictionary_calendar[selectedYear.get()] \
            and day_number in dictionary_calendar[selectedYear.get()][selectedMonth.get()]:
        for title in dictionary_calendar[selectedYear.get()][selectedMonth.get()][day_number]:
            print(title, dictionary_calendar[selectedYear.get()][selectedMonth.get()][day_number][title])
            t = title
            d = dictionary_calendar[selectedYear.get()][selectedMonth.get()][day_number][title]
            obj = MinimizableTask(leftPane, bg="white", width="100", height="100", desc=d, title=t)
            obj.grid_propagate(False)
            obj.place(x=5, y=y)
            y += 105


def double_click(event, day_number):
    if day_number != 0:
        print("Two Click, Day Number:", day_number)
        window = MakeTaskWindow()
        window.get_top().wait_window()
        print("Canceled", window.canceled, "Closed", window.closed_x)
        if not window.canceled and not window.closed_x:  # Checks if cancel button pressed or X'd out
            if check_same_title(day=day_number):  # False means it is a new title, therefore it saves
                print(window.task_title)
                print(window.task_description)
                save(title=window.task_title, desc=window.task_description, day=day_number)


def save(title, desc, day):
    global dictionary_calendar
    if selectedYear.get() not in dictionary_calendar:
        dictionary_calendar[selectedYear.get()] = dict()
    if selectedMonth.get() not in dictionary_calendar[selectedYear.get()]:
        dictionary_calendar[selectedYear.get()][selectedMonth.get()] = dict()
    if day not in dictionary_calendar[selectedYear.get()][selectedMonth.get()]:
        dictionary_calendar[selectedYear.get()][selectedMonth.get()][day] = dict()
    if title not in dictionary_calendar[selectedYear.get()][selectedMonth.get()][day]:
        dictionary_calendar[selectedYear.get()][selectedMonth.get()][day][title] = desc

    pickle_out = open("test.pickle", "wb")
    pickle.dump(dictionary_calendar, pickle_out)
    pickle_out.close()


def check_same_title(day):
    global dictionary_calendar
    if selectedYear.get() not in dictionary_calendar:
        return True
    if selectedMonth.get() not in dictionary_calendar[selectedYear.get()]:
        return True
    if day not in dictionary_calendar[selectedYear.get()][selectedMonth.get()]:
        return True
    if title not in dictionary_calendar[selectedYear.get()][selectedMonth.get()][day]:
        return True
    return False

if __name__ == "__main__":
    root = Tk()
    root.geometry("1280x720")
    root.resizable(False, False)
    root.configure()

    leftPane = PanedWindow(background="#212121", height=720, width=480)
    calendarPane = PanedWindow(background="#303030", width=800)
    leftPane.pack(fill=BOTH, side=LEFT)
    leftPane.pack_propagate(False)
    calendarPane.pack(fill=BOTH, side=RIGHT)
    calendarPane.pack_propagate(False)

    calendarFrame = Frame(calendarPane, bg="black", width=770, height=570)
    calendarFrame.place(x=15, y=100)

    scrollbar = Scrollbar(leftPane)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox = Listbox(leftPane, yscrollcommand=scrollbar.set)
    #listbox.pack(side=LEFT)
    scrollbar.config(command=listbox.yview)

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
        test = CalendarDay(calendarFrame, bg="white", borderwidth=1, width=110, height=114, relief="solid")
        # label = Label(test, text=str(35-count))
        # label.place(x=0, y=0)
        test.place(x=calX, y=calY)
        test.pack_propagate(False)
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

    # FORMAT ON START
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
            label = Label(cell, text=str(i), bg="white")
            cell.set_day(i)
            #label.place(x=0, y=0)
            label.pack(side=LEFT, anchor=N)
            if selectedYear.get() in dictionary_calendar and selectedMonth.get() in dictionary_calendar[
                selectedYear.get()] and i in dictionary_calendar[selectedYear.get()][selectedMonth.get()]:
                for title in dictionary_calendar[selectedYear.get()][selectedMonth.get()][i]:
                    task_title = Label(cell, text=title)
                    task_title.pack(anchor=W)
        cell.bind("<Double-1>", lambda event, day_number=cell.get_day(): double_click(event, day_number))
        cell.bind("<Button-1>", lambda event, day_number=cell.get_day(): one_click(event, day_number))
        i += 1


    mainloop()
