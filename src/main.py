import tkinter as tk
import calendar
import pickle

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1280x720")
    c = calendar.TextCalendar(calendar.SUNDAY)
    #print(c.formatmonth(2019,6))
    #for i in c.itermonthdays(2019,6):
    #    print(i)
    dict = {2000:"First Birthday"}

    pickle_out = open("test.pickle", "wb")
    pickle.dump(dict, pickle_out)
    pickle_out.close()

    pickle_in = open("test.pickle","rb")
    entry = pickle.load(pickle_in)
    print(entry[2000])
    #tk.mainloop()