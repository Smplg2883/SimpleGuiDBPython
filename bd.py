import sqlite3
import tkinter as tk
from tkinter import ttk
import datetime

#CreatingDB
conn = sqlite3.connect('user_database.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        registration_date DATE,
        registration_time TIME
    )
''')
conn.commit()

#AddingNewUser
def add_user():
    username = username_entry.get()
    password = password_entry.get()
    registration_date = datetime.date.today()
    registration_time = datetime.datetime.now().strftime('%H:%M:%S')
    cursor.execute("INSERT INTO users (username, password, registration_date, registration_time) VALUES (?, ?, ?, ?)",
                   (username, password, registration_date, registration_time))
    conn.commit()
    refresh_table()

#DelSelectedUsers
def delete_selected_users():
    selected_items = user_tree.selection()
    for item in selected_items:
        user_id = user_tree.item(item, "values")[0]
        cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    refresh_table()

#Refreshfunc
def refresh_table():
    for row in user_tree.get_children():
        user_tree.delete(row)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        user_tree.insert("", "end", values=user)

#SortFunc
def sort_column(col, reverse):
    data = [(user_tree.set(child, col), child) for child in user_tree.get_children('')]
    data.sort(reverse=reverse)
    for i, (val, child) in enumerate(data):
        user_tree.move(child, '', i)
    user_tree.heading(col, command=lambda: sort_column(col, not reverse))

def on_enter_key(event):
    add_user()

#MainWindow
root = tk.Tk()
root.title("DATA BASE")

#GUI
frame = ttk.Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

username_label = ttk.Label(frame, text="Login:")
username_label.grid(row=0, column=0)
username_entry = ttk.Entry(frame)
username_entry.grid(row=0, column=1)
username_entry.bind('<Return>', on_enter_key)

password_label = ttk.Label(frame, text="Password:")
password_label.grid(row=1, column=0)
password_entry = ttk.Entry(frame)
password_entry.grid(row=1, column=1)
password_entry.bind('<Return>', on_enter_key) 

add_button = ttk.Button(frame, text="ADD", command=add_user)
add_button.grid(row=0, column=2)
delete_selected_button = ttk.Button(frame, text="DELETE SELECTED", command=delete_selected_users)
delete_selected_button.grid(row=1, column=2)

user_tree = ttk.Treeview(root, columns=("ID", "LOGIN", "PASSWORD", "REGISTRATION DATE", "REGISTRATION TIME"))
user_tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
user_tree.column("#0", width=0, stretch=tk.NO)
user_tree.heading("#1", text="ID", command=lambda: sort_column("#1", False))
user_tree.heading("#2", text="LOGIN", command=lambda: sort_column("#2", False))
user_tree.heading("#3", text="PASSWORD", command=lambda: sort_column("#3", False))
user_tree.heading("#4", text="REGISTRATION DATE", command=lambda: sort_column("#4", False))
user_tree.heading("#5", text="REGISTRATION TIME", command=lambda: sort_column("#5", False))
user_tree["selectmode"] = "extended"
refresh_table()

root.grid_rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)

root.mainloop()