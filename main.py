from tkinter import *
from tkinter import messagebox, ttk
import tkinter as tk

import sqlite3

COLOR_PROGRAM = "#FFD792"

root = Tk()
root.title("База данных компьютерных компонентов")
root.geometry("665x420")
root["bg"] = COLOR_PROGRAM


class DB:
    def __init__(self):
        self.conn = sqlite3.connect("components.db")
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS components (id INTEGER PRIMARY KEY, name TEXT, component TEXT, number TEXT, date TEXT)")
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def view_component(self):
        self.cur.execute("SELECT * FROM components")
        rows = self.cur.fetchall()
        return rows

    def add_row(self, name, component, number, date):
        insert_components = "INSERT INTO components (name, component, number, date) VALUES (:name, :component, :number, :date)"
        self.cur.execute(insert_components, {"name": name, "component": component, "number": number, "date": date})
        self.conn.commit()

    def delete_row(self, id):
        self.cur.execute("DELETE FROM components WHERE id=?", (id,))
        self.conn.commit()

    def edit_row(self, name, component, number, date):
        self.cur.execute("UPDATE component SET name=?, component=?, number=?, date=? WHERE id=?",
                         (name, component, number, date, id,))
        self.conn.commit()


db = DB()


def view_command():
    for row in tree.get_children():
        tree.delete(row)

    for row in db.view_component():
        tree.insert("", "end", values=row)


def add_command():
    db.add_row(name_entry.get(), component_entry.get(), number_entry.get(), date_entry.get())
    view_command()


def delete_command():
    col = tree.focus()
    if col:
        id_num = tree.item(col)["values"][0]
        db.delete_row(id_num)
        view_command()


def edit_command():
    col = tree.focus()

    if col:
        id_num = tree.item(col)["values"][0]
        db.delete_row(id_num)
        db.add_row(name_entry.get(), component_entry.get(), number_entry.get(), date_entry.get())
        view_command()


# NAME PROGRAM
Label(text="База данных компьютерных компонентов", background=COLOR_PROGRAM, foreground="#434643", font="Arial 20 bold").grid(row=0, column=0, columnspan=3, padx=35, pady=15, sticky="EW")

# LABEL
name_label = Label(text="Марка:", background=COLOR_PROGRAM, font="Arial 10")
component_label = Label(text="Компонент:", background=COLOR_PROGRAM, font="Arial 10")
number_label = Label(text="Номер:", background=COLOR_PROGRAM, font="Arial 10")
date_label = Label(text="Дата:", background=COLOR_PROGRAM, font="Arial 10")

name_label.grid(row=1, column=0, padx=20, sticky="w")
component_label.grid(row=2, column=0, padx=20, sticky="w")
number_label.grid(row=3, column=0, padx=20, sticky="w")
date_label.grid(row=4, column=0, padx=20,sticky="w")

# ENTRY
name_entry = Entry()
component_entry = Entry()
number_entry = Entry()
date_entry = Entry()

name_entry.grid(row=1, column=0, sticky="e")
component_entry.grid(row=2, column=0, sticky="e")
number_entry.grid(row=3, column=0, sticky="e")
date_entry.grid(row=4, column=0, sticky="e")

# TREEVIEW
columns_treeview = ("id", "name", "component", "number", "date")
tree = ttk.Treeview(columns=columns_treeview, show="headings")
tree.grid(row=5, column=0, columnspan=4, rowspan=3, padx=20, pady=20, sticky='w')

tree.heading("id", text="id")
tree.heading("name", text="Марка")
tree.heading("component", text="Компонент")
tree.heading("number", text="Номер")
tree.heading("date", text="Дата")

tree.column("#1", width=10, anchor=tk.CENTER)
tree.column("#2", width=70, anchor=tk.CENTER)
tree.column("#3", width=70, anchor=tk.CENTER)
tree.column("#4", width=70, anchor=tk.CENTER)
tree.column("#5", width=70, anchor=tk.CENTER)

# BUTTONS
add_button = Button(text="Добавить", background="#afff8a", command=add_command)
delete_button = Button(text="Удалить", background="#ff998c", command=delete_command)
edit_button = Button(text="Обновить", background="#a9b6ff", command=edit_command)

add_button.grid(row=5, column=2, sticky="ew", ipady=15)
delete_button.grid(row=6, column=2, sticky="ew", ipady=15)
edit_button.grid(row=7, column=2, sticky="ew", ipady=15)

view_command()
root.mainloop()
