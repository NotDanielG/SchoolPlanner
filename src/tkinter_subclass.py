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


class MakeTaskWindow:
    def __init__(self):
        super().__init__()
        self.task_title = ""
        self.task_description = ""

        self.__top = tk.Toplevel()
        self.__top.geometry("400x250")
        self.__top.resizable(False, False)
        self.__top.title("Make New Task")
        self.__top.grab_set()

        label_title = tk.Label(self.__top, text="Title of Task:")
        label_description = tk.Label(self.__top, text="Task Description:")
        label_title.grid(row=0, column=0, sticky="E", padx=(15, 0), pady=3)
        label_description.grid(row=1, column=0, sticky="NE", padx=(15, 0))

        self.entry_title = tk.Entry(self.__top, width=40)
        self.entry_title.config(font=("arial", 10))

        self.entry_text = tk.Text(self.__top, width=40, height=10)
        self.entry_text.config(font=("arial", 10))
        self.entry_text.place(x=0, y=0)

        self.entry_title.grid(row=0, column=1, sticky="W", pady=3)
        self.entry_text.grid(row=1, column=1, sticky="W")

        button = tk.Button(self.__top, text="Save Task", command=self.save)
        button.place(x=25, y=60)

    def set_task_title(self, title):
        self.task_title = title

    def get_top(self):
        return self.__top

    def save(self):
        # print(self.entry_title.get())
        # print(self.entry_text.get("1.0", 'end-1c'))
        if len(str(self.entry_title.get())) != 0 and len(self.entry_text.get("1.0", 'end-1c')) != 0:
            self.task_title = str(self.entry_title.get())
            self.task_description = self.entry_text.get("1.0", 'end-1c')
            self.__top.destroy()
