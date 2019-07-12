from tkinter import *
import calendar
import pickle

def optionChanged(*args):
    print(monthChoice[selectedMonth.get()])
    print(selectedYear.get())
    print(selectedDay.get())

    dayList = range(1, calendar.monthrange(int(selectedYear.get()), int(monthChoice[selectedMonth.get()]))[1])
    #dayChange(dayList)

def dayChange(*args):
    print("1")

if __name__ == '__main__':
    root = Tk()
    root.geometry("1280x720")
    root.resizable(False,False)
    root.configure()
    c = calendar.TextCalendar(calendar.SUNDAY)
    #print(c.formatmonth(2019,6))
    #for i in c.itermonthdays(2019,6):
    #    print(i)
    dict = {}
    dict_day = {1:"Task One"}
    dict_month = {"January":dict_day}
    dict[2000] = dict_month

    d_d = {2:"Task Two"}
    d_m = {"March":d_d}
    dict[2001] = d_m

    pickle_out = open("test.pickle", "wb")
    pickle.dump(dict, pickle_out)
    pickle_out.close()

    pickle_in = open("test.pickle","rb")
    #entry = pickle.load(pickle_in)

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
        test = Frame(calendarPane, bg="green", width=110,height=25)
        test.place(x=calX, y=calY)
        label = Label(test, text=name)
        #label.pack(side="right")
        label.place(x=60, y=0)
        label.place(x=110-label.winfo_reqwidth())
        calX += 110

    count = 35
    calX = 0
    calY = 0
    while count >= 0:
        test = Frame(calendarFrame, bg="blue", borderwidth=1, width=110, height=114)
        label = Label(test, text=str(35-count))
        label.place(x=0,y=0)
        test.place(x=calX, y=calY)
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
    selectedMonth.trace("w", optionChanged)

    monthMenu = OptionMenu(calendarPane, selectedMonth, *monthChoice)
    monthMenu.place(x=315, y=10)
    monthMenu.config(width=10, indicator=0)

    yearList = range(2019,2030)
    yearChoice = {}
    for year in yearList:
        yearChoice[year] = year
    selectedYear = StringVar()
    selectedYear.set(list(yearChoice.keys())[0])
    selectedYear.trace("w", optionChanged)

    yearMenu = OptionMenu(calendarPane, selectedYear, *yearChoice)
    yearMenu.place(x=455, y=10)
    yearMenu.config(width=10, indicator=0)

    #monthrange 0 = monday
    dayList = range(1, calendar.monthrange(int(selectedYear.get()), int(monthChoice[selectedMonth.get()]))[1])
    print(dayList)
    dayChoice = {}
    for day in dayList:
        dayChoice[day] = day
    selectedDay = IntVar()
    selectedDay.set(list(dayChoice.keys())[0])
    selectedDay.trace("w", dayChange)

    dayMenu = OptionMenu(calendarPane, selectedDay, *dayChoice)
    dayMenu.place(x=400, y=10)
    dayMenu.config(width=5, indicator=0)


    mainloop()