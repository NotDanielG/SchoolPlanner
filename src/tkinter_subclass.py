import tkinter as tk
import os

def hello():
    print("hello")


class CalendarDay(tk.Frame):
    def __init__(self, root, bg, borderwidth, width, height, relief):
        tk.Frame.__init__(self, root, bg=bg, borderwidth=borderwidth, width=width, height=height, relief=relief)
        self.day = 0
        self.task_list = list()

    def get_day(self):
        return self.day

    def set_day(self, day):
        self.day = day

    def append_task(self, task):
        self.task_list.append(task)


class MakeTaskWindow:
    def __init__(self):
        super().__init__()
        self.task_title = ""
        self.task_description = ""
        self.canceled = False
        self.closed_x = True

        self.__top = tk.Toplevel(bg="#121212")
        self.__top.geometry("400x250")
        self.__top.resizable(False, False)
        self.__top.title("Make New Task")
        self.__top.grab_set()

        label_title = tk.Label(self.__top, text="Title of Task:", bg="#424242", fg="white")
        label_description = tk.Label(self.__top, text="Task Description:", bg="#424242", fg="white")
        label_title.grid(row=0, column=0, sticky="E", padx=(15, 5), pady=3)
        label_description.grid(row=1, column=0, sticky="NE", padx=(15, 5))

        self.entry_title = tk.Entry(self.__top, width=39)
        self.entry_title.config(font=("arial", 10))

        self.entry_text = tk.Text(self.__top, width=39, height=10)
        self.entry_text.config(font=("arial", 10))
        self.entry_text.place(x=0, y=0)

        self.entry_title.grid(row=0, column=1, sticky="W", pady=3)
        self.entry_text.grid(row=1, column=1, sticky="W")

        button = tk.Button(self.__top, text="Save Task", command=self.save, width=8)
        button.place(x=250, y=220)

        button = tk.Button(self.__top, text="Cancel", command=self.cancel, width=5)
        button.place(x=335, y=220)

    def set_task_title(self, title):
        self.task_title = title

    def get_top(self):
        return self.__top

    def save(self):
        if len(str(self.entry_title.get())) != 0 and len(self.entry_text.get("1.0", 'end-1c')) != 0:
            self.task_title = str(self.entry_title.get())
            self.task_description = self.entry_text.get("1.0", 'end-1c')
            self.closed_x = False
            self.__top.destroy()

    def is_empty(self):
        if len(str(self.entry_title.get())) != 0 and len(self.entry_text.get("1.0", 'end-1c')) != 0:
            return False
        return True

    def cancel(self):
        self.canceled = True
        self.closed_x = False
        self.__top.destroy()


class MinimizableTask(tk.Frame):
    def __init__(self, root, bg, width, height, desc):
        tk.Frame.__init__(self, root, bg=bg, width=width, height=height)
        self.description = desc
        self.image_files = list()
        dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        the_dir = os.path.join(dir, "resources\smaller_expand.png")
        self.image_files.append(the_dir)
        the_dir = os.path.join(dir, "resources\min.png")
        self.image_files.append(the_dir)

        temp = tk.PhotoImage(file=self.image_files[0])
        self.min_button = tk.Label(self, image=temp, bg=self["background"])
        self.min_button.image = temp
        self.min_button.pack(side=tk.LEFT)
        self.min_button.bind("<Button-1>", self.eggsdee)

    def eggsdee(self, event):
        print("Working")
