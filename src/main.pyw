from tkinter import *
import calendar
import pickle
from tkinter_subclass import *
from datetime import date

try:  # First thing done, dictionary_calendar is a mult nested dictionary. [Years][Months][Days][Titles][Description]
    pickle_in = open("test.pickle", "rb")
    entry = pickle.load(pickle_in)
    dictionary_calendar = entry
except EOFError:
    dictionary_calendar = dict()  # If empty, creates new dict


def update_calender():  # repeat of option changed, aside from args
    cal_range = calendar.monthrange(int(selectedYear.get()), int(monthChoice[selectedMonth.get()]))
    cells = dayCells
    counter = cal_range[0] + 1
    if counter >= 7:
        counter = 0
    k = 0
    is_start = False
    for cell in cells:
        for child in cell.winfo_children():
            child.destroy()
        if k == counter and not is_start:
            is_start = True
            k = 1
        if is_start and k <= cal_range[1]:
            label = Label(cell, text=str(k), bg="white")
            cell.set_day(k)
            label.pack(side=LEFT, anchor=N)
            if selectedYear.get() in dictionary_calendar and selectedMonth.get() in dictionary_calendar[
                selectedYear.get()] and k in dictionary_calendar[selectedYear.get()][selectedMonth.get()]:
                for title in dictionary_calendar[selectedYear.get()][selectedMonth.get()][k]:
                    task_title = Label(cell, text=title)
                    task_title.pack(anchor=W)
        if not is_start or k > cal_range[1]:
            cell.set_day(0)
        cell.bind("<Button-3>", lambda event, day_number=cell.get_day(): right_click(event, day_number))
        cell.bind("<Button-1>", lambda event, day_number=cell.get_day(): one_click(event, day_number))
        k += 1
    for obj in task_list:
        obj.destroy()


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
                    selectedYear.get()] and j in dictionary_calendar[selectedYear.get()][selectedMonth.get()]:
                for title in dictionary_calendar[selectedYear.get()][selectedMonth.get()][j]:
                    task_title = Label(cell, text=title)
                    task_title.pack(anchor=W)
        if not start or j > range[1]:
            cell.set_day(0)
        cell.bind("<Button-3>", lambda event, day_number=cell.get_day(): right_click(event, day_number))
        cell.bind("<Button-1>", lambda event, day_number=cell.get_day(): one_click(event, day_number))
        j += 1
    for obj in task_list:
        obj.destroy()

    for label in dayPane.winfo_children():
        label.destroy()
    daySelected=1
    new_label = Label(dayPane, bg=dayPane["background"], fg="white", font=("Helvetica", 24),
                      text=(selectedMonth.get(), str(daySelected), selectedYear.get()))
    new_label.pack()
    view_task(daySelected)


def one_click(event, day_number):
    # Use day number, month and year to find tasks and respective description
    if day_number != 0:
        global dictionary_calendar
        for lab in dayPane.winfo_children():
            lab.destroy()
        daySelected = day_number
        day_label = Label(dayPane, bg=dayPane["background"], fg="white", font=("Helvetica", 24),
                          text=(selectedMonth.get(), str(daySelected), selectedYear.get()))
        day_label.pack()
        for obj in task_list:
            obj.destroy()
        if selectedYear.get() in dictionary_calendar and selectedMonth.get() in dictionary_calendar[selectedYear.get()] \
                and day_number in dictionary_calendar[selectedYear.get()][selectedMonth.get()]:
            view_task(day_number=day_number)


def view_task(day_number):
    d = ""  # desc
    t = ""  # title
    y = 5
    if selectedYear.get() in dictionary_calendar and selectedMonth.get() in dictionary_calendar[selectedYear.get()] \
            and day_number in dictionary_calendar[selectedYear.get()][selectedMonth.get()]:
        for title in dictionary_calendar[selectedYear.get()][selectedMonth.get()][day_number]:
            t = title
            d = dictionary_calendar[selectedYear.get()][selectedMonth.get()][day_number][title]
            obj = MinimizableTask(taskPane, bg="#484848", width=440, desc=d, title=t)
            obj.pack(anchor=W, padx=5, pady=5)
            obj.bind("<Double-1>", lambda event, day=day_number, title=obj.title, desc=d: change_task(event, day, title, desc))
            task_list.append(obj)
            y += 105


def change_task(event, day, title, desc):
    top_window = ChangeTaskWindow()
    top_window.top.wait_window()
    if top_window.is_edit:
        change_memory(mode=0, day=day, title=title, desc=desc)
    if top_window.is_delete:
        change_memory(mode=1, day=day, title=title, desc=desc)


def change_memory(mode, day, title, desc):  # 0 is edit, 1 is delete
    global dictionary_calendar
    # print("Mode= ", mode, "Day= ", day)
    old_title = title
    if mode == 0:
        window = MakeTaskWindow(mode=1, old_desc=desc, old_title=title)
        window.get_top().wait_window()
        if not window.canceled and not window.closed_x:
            dictionary_calendar[selectedYear.get()][selectedMonth.get()][day].pop(old_title)
            if check_same_title(day=day, task_title=window.task_title):
                new_title = window.task_title
                new_desc = window.task_description
                save(title=new_title, desc=new_desc, day=day)
                view_task(day_number=day)
    if mode == 1:
        dictionary_calendar[selectedYear.get()][selectedMonth.get()][day].pop(old_title)
        pickle_out = open("test.pickle", "wb")
        pickle.dump(dictionary_calendar, pickle_out)
        pickle_out.close()
        update_calender()


def right_click(event, day_number):
    if day_number != 0:
        # print("Two Click, Day Number:", day_number)
        window = MakeTaskWindow(mode=0, old_desc="", old_title="")
        window.get_top().wait_window()
        if not window.canceled and not window.closed_x:  # Checks if cancel button pressed or X'd out
            if check_same_title(day=day_number, task_title=window.task_title):  # False means it is a new title, therefore it saves
                # print(window.task_title)
                # print(window.task_description)
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

    update_calender()


def check_same_title(day, task_title):
    global dictionary_calendar
    if selectedYear.get() not in dictionary_calendar:
        return True
    if selectedMonth.get() not in dictionary_calendar[selectedYear.get()]:
        return True
    if day not in dictionary_calendar[selectedYear.get()][selectedMonth.get()]:
        return True
    if task_title not in dictionary_calendar[selectedYear.get()][selectedMonth.get()][day]:
        return True
    return False


if __name__ == "__main__":
    root = Tk()
    root.geometry("1280x720")
    root.resizable(False, False)
    root.title("School Planner")
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    icon = os.path.join(path, "resources\calendar_icon.ico")
    root.iconbitmap(icon)
    root.configure()

    leftPane = PanedWindow(background="#141414", height=720, width=480)  # Where task and day selected appears
    calendarPane = PanedWindow(background="#212121", width=800)  # Holds the calendar
    leftPane.pack(fill=BOTH, side=LEFT)
    leftPane.pack_propagate(False)
    calendarPane.pack(fill=BOTH, side=RIGHT)
    calendarPane.pack_propagate(False)

    dayPane = Frame(leftPane, bg="#2e2e2e", width=450, height=48)
    dayPane.place(x=5, y=5)
    dayPane.pack_propagate(False)
    daySelected = 1
    taskPane = Frame(leftPane, bg="#2e2e2e", width=450, height=655)
    taskPane.place(x=5, y=58)
    taskPane.pack_propagate(False)
    calendarFrame = Frame(calendarPane, bg="#2e2e2e", width=770, height=570)
    calendarFrame.place(x=15, y=100)

    task_list = list()  # Not used yet
    scrollbar = Scrollbar(leftPane)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox = Listbox(leftPane, yscrollcommand=scrollbar.set)
    #listbox.pack(side=LEFT)
    scrollbar.config(command=listbox.yview)

    calX = 15
    calY = 75

    dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    for name in dayNames:  # List the days on top of the calendar
        test = Frame(calendarPane, bg="#2e2e2e", width=110, height=25)
        test.place(x=calX, y=calY)
        label = Label(test, text=name, bg=test["background"], fg="white")
        label.place(x=60, y=0)
        label.place(x=110-label.winfo_reqwidth())
        calX += 110

    count = 34
    calX = 0
    calY = 0
    dayCells = list()  # Holds each cell/day, each cell has a day number associated with it
    while count >= 0:  # separates the cells of the days of the week
        test = CalendarDay(calendarFrame, bg="white", borderwidth=1, width=110, height=114, relief="solid")
        test.place(x=calX, y=calY)
        test.pack_propagate(False)
        dayCells.append(test)
        calX += 110
        if count % 7 == 0 and count != 35:
            calY += 114
            calX = 0
        count += -1

    open_day = date.today()  # Sets to current month and year
    today_month = open_day.strftime("%B")
    today_year = open_day.strftime("%Y")

    monthChoice = {}
    count = 1
    for month in calendar.month_name:  # sets month choice for the options
        if month != "":
            monthChoice[month] = count
            count += 1
    selectedMonth = StringVar()
    selectedMonth.set(today_month)
    selectedMonth.trace("w", lambda name, index, mode, dayCells=dayCells: option_changed(dayCells))

    monthMenu = OptionMenu(calendarPane, selectedMonth, *monthChoice)
    monthMenu.place(x=315, y=10)
    monthMenu.config(width=10, indicator=0)

    yearList = range(2019, 2030)
    yearChoice = {}
    for year in yearList:  # sets year choices
        yearChoice[year] = year
    selectedYear = StringVar()
    selectedYear.set(today_year)
    selectedYear.trace("w", lambda name, index, mode, dayCells=dayCells: option_changed(dayCells))

    yearMenu = OptionMenu(calendarPane, selectedYear, *yearChoice)
    yearMenu.place(x=455, y=10)
    yearMenu.config(width=10, indicator=0)

    # FORMAT ON START
    dayList = range(1, calendar.monthrange(int(selectedYear.get()), int(monthChoice[selectedMonth.get()]))[1])
    monRange = calendar.monthrange(int(selectedYear.get()), int(monthChoice[selectedMonth.get()]))

    count = monRange[0] + 1  # Loop sets the calendar days
    if count >= 7:
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
        cell.bind("<Button-3>", lambda event, day_number=cell.get_day(): right_click(event, day_number))
        cell.bind("<Button-1>", lambda event, day_number=cell.get_day(): one_click(event, day_number))
        i += 1

    new_label = Label(dayPane, bg=dayPane["background"], fg="white", font=("Helvetica", 24),
                      text=(selectedMonth.get(), str(daySelected), selectedYear.get()))
    new_label.pack()

    mainloop()
