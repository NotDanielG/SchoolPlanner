import tkinter

class calendarDay(tkinter.Frame):
    def __init__(self, master, background, width, height, day):
        super().__init__(self, master, bgd=background, width=width, height = height)
        self.day = day
    def get_day(self):
        return self.day