import tkinter


def hello():
    print("hello")


class calendar_day(tkinter.Frame):
    def __init__(self, root, bg, borderwidth, width, height):
        tkinter.Frame.__init__(self, root, bg=bg, borderwidth=borderwidth, width=width, height=height)
        self.day = 0

    def get_day(self):
        return self.day

    def set_day(self, day):
        self.day = day
