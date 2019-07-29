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

        self.top = tk.Toplevel()
        self.top.geometry("300x400")
        self.top.title("Make New Task")
        label_title = tk.Label(self.top, text="Title of Task:")
        label_description = tk.Label(self.top, text="Task Description:")
        label_title.grid(row=0, column=0, sticky="E", padx=(15, 0))
        label_description.grid(row=1, column=0, sticky="NE", padx=(15, 0))

        self.entry_title = tk.Entry(self.top)
        self.entry_title.config(font=("arial", 10))

        textbox_holder = tk.Frame(self.top)
        print(textbox_holder.winfo_reqwidth())
        textbox_holder.grid_propagate(True)
        self.entry_text = tk.Text(textbox_holder)
        self.entry_text.config(font=("arial", 10))
        self.entry_text.place(x=0, y=0)

        self.entry_title.grid(row=0, column=1, sticky="W")
        textbox_holder.grid(row=1, column=1, sticky="W")

        button = tk.Button(self.top, text="Save Task", command=self.save)

        button.place(x=25, y=300)

    def set_task_title(self, title):
        self.task_title = title

    def save(self):
        print(self.entry_title.get())
        self.task_title = str(self.entry_title.get())
        print(self.entry_text.get("1.0", 'end-1c'))
        self.top.destroy()
