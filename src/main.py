from tkinter import *
import calendar
import pickle

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

    monthChoice = []
    for month in calendar.month_name:
        if month != "":
            monthChoice.append(month)
    selectedMonth = StringVar()
    selectedMonth.set(monthChoice[0])
    monthMenu = OptionMenu(calendarPane, selectedMonth, *monthChoice)
    monthMenu.place(x=335, y=10)
    monthMenu.config(width=10, indicator=0)
    mainloop()