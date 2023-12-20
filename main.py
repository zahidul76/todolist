import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
import requests
from io import BytesIO

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("800x600")

        # Download the image from the URL
        image_url = "https://wallpapers.com/images/hd/wooden-cottage-sea-high-resolution-d7fahhz6phtkdveh.webp"
        response = requests.get(image_url)
        self.background_image = Image.open(BytesIO(response.content))
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Database connection and table creation
        self.conn = sqlite3.connect("todo.db")
        self.create_table()

        # Entry widget for task input
        self.task_entry = tk.Entry(root, font=("Helvetica", 14))
        self.task_entry.place(relx=0.5, rely=0.1, anchor="n")

        # Button to add tasks
        add_button = tk.Button(root, text="Add Task", command=self.add_task)
        add_button.place(relx=0.5, rely=0.2, anchor="n")

        # Listbox to display tasks
        self.task_listbox = tk.Listbox(root, font=("Helvetica", 12), selectbackground="lightblue", selectmode=tk.SINGLE)
        self.task_listbox.place(relx=0.5, rely=0.4, anchor="n")

        # Button to delete selected task
        delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        delete_button.place(relx=0.5, rely=0.8, anchor="n")

        # Button to exit the application
        exit_button = tk.Button(root, text="Exit", command=root.destroy)
        exit_button.place(relx=0.95, rely=0.95, anchor="se")

        # Load tasks from the database
        self.load_tasks()

    def create_table(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL
                )
            """)

    def load_tasks(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM tasks")
            tasks = cursor.fetchall()
            for task in tasks:
                self.task_listbox.insert(tk.END, task[1])

    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task_text,))
            self.task_listbox.insert(tk.END, task_text)
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            selected_task = self.task_listbox.get(selected_task_index)
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM tasks WHERE task=?", (selected_task,))
            self.task_listbox.delete(selected_task_index)
        else:
            messagebox.showwarning("Warning", "Please select a task to delete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
