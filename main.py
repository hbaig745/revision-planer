from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno

import os
import sys
import subprocess

subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
from PIL import Image, ImageTk


import random

array = []
topic_array = []
widgets = {}


def logout():
    tabs.tab(0, state=NORMAL)
    tabs.select(0)
    tabs.tab(1, state=DISABLED)


def add_topic_func():
    if add_topic.get() != "":
        with open(f"{current_sub}.txt", "a") as f:
            f.write(add_topic.get() + ",")

        add_topic.delete(0, END)
        add_topic.insert(0, "")

        get_topics()
        topic_list.set(str(topic_array))


def delete_topic_func():
    answer = askyesno("Confirmation", "Are you sure you want to delete this topic?")
    if answer:
        get_topics()
        if delete_topic.get() != "":
            with open(f"{current_sub}.txt", "w") as f:
                try:
                    topic_array.remove(delete_topic.get())
                except:
                    pass

                for a in topic_array:
                    f.write(f"{a},")

                delete_topic.set("")

        topic_list.set(str(topic_array))


def get_topics():
    global topic_array
    with open(f"{current_sub}.txt", "r") as f:
        for line in f:
            topic_array = line.split(",")

    try:
        del topic_array[-1]
    except:
        pass

    delete_topic["values"] = topic_array
    topic_list.set(str(topic_array))


def random_topic_func():
    get_topics()
    try:
        random_topic.set(topic_array[random.randint(0, len(topic_array) - 1)])
    except:
        pass


def update_list():
    topic_list.set(str(topic_array))


def restart():
    sys.stdout.flush()
    os.execl(sys.executable, "python", __file__, *sys.argv[1:])


def delete_subject():
    answer = askyesno("Confirmation", "Are you sure you want to delete this subject?")
    if answer:
        if delete_combo.get() != "":
            with open("subjects.txt", "w") as f:
                try:
                    array.remove(delete_combo.get())
                except:
                    pass

                for e in array:
                    f.write(f"{e},")

            current_sub = delete_combo.get()
            os.remove(f"{current_sub}.txt")
            delete_combo.set("")
            login_combo.set("")
            register_entry.delete(0, END)
            register_entry.insert(0, "")


def login():
    global current_sub
    current_sub = login_combo.get()
    tabs.tab(1, state=NORMAL)
    tabs.select(1)
    tabs.tab(0, state=DISABLED)
    get_topics()

    delete_combo.set("")
    login_combo.set("")
    register_entry.delete(0, END)
    register_entry.insert(0, "")


def get_subjects():
    global array
    with open("subjects.txt", "r") as f:
        for line in f:
            array = line.split(",")
    try:
        del array[-1]
    except:
        pass
    login_combo["values"] = array
    delete_combo["values"] = array


def register():
    if register_entry.get() != "":
        with open("subjects.txt", "a") as f:
            f.write(f"{register_entry.get()},")

        f = open(f"{register_entry.get()}.txt", "w")
        f.close()

        delete_combo.set("")
        login_combo.set("")
        register_entry.delete(0, END)
        register_entry.insert(0, "")


def quit_button():
    answer = askyesno("Confirmation", "Are you sure you want to quit?")
    if answer:
        root.destroy()


root = Tk()
root.title("Revision Program")

root.geometry("700x500")
root.resizable(0, 0)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

main = ttk.Frame(root, padding=3)
main.grid(sticky=NSEW)

main.columnconfigure(0, weight=1)
main.rowconfigure(0, weight=1)

tabs = ttk.Notebook(main)
tabs.grid(sticky=NSEW)

login_tab = ttk.Frame(tabs, padding="3 1 6 5")
subject_tab = ttk.Frame(tabs, padding="3 1 6 5")

tabs.add(login_tab, text="LOGIN")
tabs.add(subject_tab, text="SUBJECT")

tabs.tab(1, state=DISABLED)

login_tab.columnconfigure(0, weight=1)
login_tab.columnconfigure(1, weight=1)
login_tab.columnconfigure(2, weight=1)
login_tab.rowconfigure(0, weight=50)
login_tab.rowconfigure(1, weight=1)
login_tab.rowconfigure(2, weight=1)

login_frame = ttk.LabelFrame(
    login_tab, text="PICK A SUBJECT", relief="groove", padding=5
)
register_frame = ttk.LabelFrame(
    login_tab, text="ADD SUBJECT", relief="groove", padding=5
)
delete_subject_frame = ttk.LabelFrame(
    login_tab, text="DELETE SUBJECT", relief="groove", padding=5
)

login_frame.grid(row=0, column=0, sticky=NSEW)
register_frame.grid(row=0, column=1, sticky=NSEW)
delete_subject_frame.grid(row=0, column=2, sticky=NSEW)


login_frame.rowconfigure(0, weight=5)
login_frame.rowconfigure(1, weight=1)
login_frame.rowconfigure(2, weight=1)
login_frame.columnconfigure(0, weight=1)

register_frame.rowconfigure(0, weight=5)
register_frame.rowconfigure(1, weight=1)
register_frame.rowconfigure(2, weight=1)
register_frame.columnconfigure(0, weight=1)

delete_subject_frame.rowconfigure(0, weight=5)
delete_subject_frame.rowconfigure(1, weight=1)
delete_subject_frame.rowconfigure(2, weight=1)
delete_subject_frame.columnconfigure(0, weight=1)

with open("subjects.txt", "r") as f:
    for line in f:
        array = line.split(",")
try:
    del array[-1]
except:
    pass
login_combo = ttk.Combobox(
    login_frame, width=30, state="readonly", values=array, postcommand=get_subjects
)
login_combo.grid(row=1)
register_entry = ttk.Entry(register_frame, width=30)
register_entry.grid(row=1)
delete_combo = ttk.Combobox(
    delete_subject_frame,
    width=30,
    state="readonly",
    values=array,
    postcommand=get_subjects,
)
delete_combo.grid(row=1)

ttk.Button(login_frame, width=50, command=login, text="SELECT").grid(row=2)
ttk.Button(register_frame, width=50, command=register, text="ADD").grid(row=2)
ttk.Button(delete_subject_frame, width=50, command=delete_subject, text="DELETE").grid(
    row=2
)

ttk.Button(login_tab, command=restart, text="RESTART").grid(
    row=1, sticky=EW, columnspan=3
)
ttk.Button(login_tab, command=quit_button, text="QUIT").grid(
    row=2, sticky=EW, columnspan=3
)

subject_tab.rowconfigure(0, weight=1)
subject_tab.rowconfigure(1, weight=1)
subject_tab.rowconfigure(2, weight=1)

subject_tab.columnconfigure(0, weight=1)
subject_tab.columnconfigure(1, weight=1)

logout_frame = ttk.LabelFrame(subject_tab, text="Logout", relief="groove", padding=5)
logout_frame.grid_propagate(False)
logout_frame.rowconfigure(0, weight=10)
logout_frame.rowconfigure(1, weight=1)
logout_frame.columnconfigure(0, weight=1)

img = ImageTk.PhotoImage(Image.open("download.jpg").resize((200, 100)))
widgets["gintoki"] = img
Label(logout_frame, image=widgets["gintoki"], relief="groove", borderwidth=2).grid()
Button(logout_frame, text="Logout", command=logout).grid(row=1, sticky=NSEW)
logout_frame.grid(row=0, column=0, sticky=NSEW)

random_frame = ttk.LabelFrame(
    subject_tab, text="Random Topic", relief="groove", padding=5
)
random_frame.grid_propagate(False)
random_frame.rowconfigure(0, weight=20)
random_frame.rowconfigure(1, weight=1)
random_frame.columnconfigure(0, weight=1)

random_topic = StringVar()
Label(random_frame, textvariable=random_topic, relief="groove").grid(row=0)

ttk.Button(random_frame, text="RANDOM", command=random_topic_func).grid(row=1)
random_frame.grid(row=1, column=0, sticky=NSEW)

add_topic_frame = ttk.LabelFrame(
    subject_tab, text="Add Topic", relief="groove", padding=5
)
add_topic_frame.grid_propagate(False)
add_topic_frame.rowconfigure(0, weight=5)
add_topic_frame.rowconfigure(1, weight=1)
add_topic_frame.columnconfigure(0, weight=1)

add_topic = Entry(add_topic_frame, width=30)
add_topic.grid()
ttk.Button(add_topic_frame, text="ADD", command=add_topic_func).grid(row=1)
widgets["add_topic"] = add_topic
add_topic_frame.grid(row=0, column=1, sticky=NSEW)

delete_topic_frame = ttk.LabelFrame(
    subject_tab, text="Delete Topic", relief="groove", padding=5
)
delete_topic_frame.grid_propagate(False)
delete_topic_frame.rowconfigure(0, weight=5)
delete_topic_frame.rowconfigure(1, weight=1)
delete_topic_frame.columnconfigure(0, weight=1)

delete_topic = ttk.Combobox(
    delete_topic_frame, values=topic_array, postcommand=get_topics, state="readonly"
)
delete_topic.grid()
ttk.Button(delete_topic_frame, text="DELETE", command=delete_topic_func).grid(row=1)
delete_topic_frame.grid(row=1, column=1, sticky=NSEW)

list_frame = ttk.LabelFrame(subject_tab, text="List Topics", relief="groove", padding=5)
list_frame.grid_propagate(False)
list_frame.rowconfigure(0, weight=5)
list_frame.rowconfigure(1, weight=1)
list_frame.columnconfigure(0, weight=1)

topic_list = StringVar()
update_list()
Label(list_frame, textvariable=topic_list, relief="groove").grid(row=0)

ttk.Button(list_frame, text="REFRESH", command=restart).grid(row=1)
list_frame.grid(row=2, column=0, sticky=NSEW, columnspan=2)

root.mainloop()
