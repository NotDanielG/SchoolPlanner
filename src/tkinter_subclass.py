from tkinter import *
import os

def hello():
    print("hello")


class CalendarDay(Frame):
    def __init__(self, root, bg, borderwidth, width, height, relief):
        Frame.__init__(self, root, bg=bg, borderwidth=borderwidth, width=width, height=height, relief=relief)
        self.day = 0
        self.task_list = list()

    def get_day(self):
        return self.day

    def set_day(self, day):
        self.day = day

    def append_task(self, task):
        self.task_list.append(task)


class MakeTaskWindow:
    def __init__(self, mode, old_title, old_desc):  # mode types: 0=create, 1=edit
        # super().__init__()
        self.task_title = ""
        self.task_description = ""
        self.canceled = False
        self.closed_x = True
        self.mode = mode

        self.__top = Toplevel(bg="#191919")
        self.__top.geometry("400x250")
        self.__top.resizable(False, False)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon = os.path.join(path, "resources\calendar_icon.ico")
        self.__top.iconbitmap(icon)
        self.__top.title("Make New Task")
        self.__top.grab_set()

        label_title = Label(self.__top, text="Title of Task:", bg="#2e2e2e", fg="white")
        label_description = Label(self.__top, text="Task Description:", bg="#2e2e2e", fg="white")
        label_title.grid(row=0, column=0, sticky="E", padx=(15, 5), pady=3)
        label_description.grid(row=1, column=0, sticky="NE", padx=(15, 5))

        self.entry_title = Entry(self.__top, width=39)
        self.entry_title.config(font=("arial", 10))

        self.entry_text = Text(self.__top, width=39, height=10)
        self.entry_text.config(font=("arial", 10))
        self.entry_text.place(x=0, y=0)

        self.entry_title.grid(row=0, column=1, sticky="W", pady=3)
        self.entry_text.grid(row=1, column=1, sticky="W")

        if self.mode == 0:
            button = Button(self.__top, text="Save Task", command=self.save, width=8)
            button.place(x=250, y=220)
        else:
            self.entry_title.insert(0, old_title)
            self.entry_text.insert("1.0", old_desc)
            button = Button(self.__top, text="Edit Task", command=self.save, width=8)
            button.place(x=250, y=220)

        button = Button(self.__top, text="Cancel", command=self.cancel, width=5)
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


class MinimizableTask(Frame):
    def __init__(self, root, bg, width, desc, title):
        Frame.__init__(self, root, bg=bg, width=width)
        self.image_files = list()
        dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        the_dir = os.path.join(dir, "resources\smaller_expand.png")
        self.image_files.append(the_dir)
        the_dir = os.path.join(dir, "resources\smaller_min.png")
        self.image_files.append(the_dir)

        self.counter = 1
        self.is_hidden = False
        temp = PhotoImage(file=self.image_files[self.counter])
        self.min_button = Label(self, image=temp, bg=self["background"])
        self.min_button.image = temp
        self.min_button.grid(row=0, column=0)
        self.min_button.bind("<Button-1>", self.button_pressed)
        self.delete_window = None

        self.description = desc
        self.title = title
        self.title_label = Label(self, text=title, bg="#626262", fg="white")
        self.title_label.config(pady=5)
        self.description_label = Label(self, text=desc, bg="#626262", fg="white")
        self.description_label.config(pady=5)
        self.title_label.grid(row=0, column=1, pady=5, padx=(0, 5))
        self.description_label.grid(row=1, column=1, pady=5, padx=(0, 5))

    def button_pressed(self, event):
        self.counter += 1
        new_image = PhotoImage(file=self.image_files[self.counter % 2])
        self.min_button.config(image=new_image)
        self.min_button.image = new_image
        if not self.is_hidden:
            self.description_label.grid_forget()
            self.is_hidden = True
        else:
            self.description_label.grid(row=1, column=1, pady=5, padx=(0, 5))
            self.is_hidden = False
        self.update()


class ChangeTaskWindow():
    def __init__(self):
        self.top = Toplevel(bg="#424242")
        self.top.title("Task Changer")
        self.top.geometry("240x80")
        self.top.resizable(False, False)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon = os.path.join(path, "resources\calendar_icon.ico")
        self.top.iconbitmap(icon)
        self.is_delete = False
        self.is_edit = False
        self.delete_label = Label(self.top, text="Delete Task?", bg="#424242", fg="white", pady=15)
        self.delete_label.pack()
        self.delete_button = Button(self.top, text="Delete", command=self.delete_task)
        self.edit_button = Button(self.top, text="Edit", command=self.edit_task)
        self.no_button = Button(self.top, text="Cancel", command=self.cancel)
        self.edit_button.pack(side=RIGHT, padx=5, pady=(0, 5), anchor=S)
        self.delete_button.pack(side=RIGHT, padx=(5, 0), pady=(0, 5), anchor=S)
        self.no_button.pack(side=RIGHT, pady=(0, 5), anchor=S)

    def edit_task(self):
        self.is_edit = True
        self.top.destroy()

    def delete_task(self):
        self.is_delete = True
        self.top.destroy()

    def cancel(self):
        self.top.destroy()
