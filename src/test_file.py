import tkinter

def hello():
    print("hello")

class calendar_day(tkinter.Frame):
    def __init__(self, root, bg, width, height, day):
        super().__init__(root, bg=bg, width=width, height=height)
        self.day = day