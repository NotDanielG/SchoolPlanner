import tkinter as tk


def hello():
    print("hello")


class CalendarDay(tk.Frame):
    def __init__(self, root, bg, borderwidth, width, height):
        tk.Frame.__init__(self, root, bg=bg, borderwidth=borderwidth, width=width, height=height)
        self.day = 0

    def get_day(self):
        return self.day

    def set_day(self, day):
        self.day = day


class MakeTaskWindow():
    def __init__(self):
        super().__init__()
        self.task_title = ""
        self.task = list()
        top = tk.Toplevel()
        top.geometry("300x400")
        top.title("Make New Task")
        label_title = tk.Label(top, text="Title of Task:")
        label_description = tk.Label(top, text="Task Description:")
        label_title.grid(row=0, column=0, sticky="E")
        label_description.grid(row=1, column=0, sticky="NE")

        entry_title = tk.Entry(top)
        entry_title.config(font=("arial", 10))
        entry_text = tk.Text(top)
        entry_text.config(font=("arial", 10))

        entry_title.grid(row=0, column=1, sticky="W")
        entry_text.grid(row=1, column=1, sticky="W")

        button = tk.Button(top, text="Save Task")
        button.config(command=lambda title=entry_title.get(), desc=entry_text.get(1.0, "end-1c"):
                      self.save(title, desc))

        button.place(x=5, y=100)
    def set_task_title(self, title):
        self.task_title = title

    def append_task(self, task):
        self.task.append(task)

    def save(self, title, desc):
        print("1")
        print(title)
        print(desc)
