import tkinter as tk
from tkinter import messagebox
import os

TASK_FILE = "tasks.txt"

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):

        if os.path.exists(TASK_FILE):
            with open(TASK_FILE, "r") as file:
                self.tasks = [line.strip() for line in file.readlines()]

    def save_tasks(self):
        i=1
        with open(TASK_FILE, "w") as file:
            for task in self.tasks:
                text = f"{i}.{task}  \n"
                file.write(text)
                i=i+1

    def add_task(self, task):

        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, task):

        self.tasks.remove(task)
        self.save_tasks()

    def update_task(self, old_task, new_task):

        idx = self.tasks.index(old_task)
        self.tasks[idx] = new_task
        self.save_tasks()


class ToDoApp:
    def __init__(self,root):
        self.root = root
        self.root.title("To-Do List")
        self.task_manager = TaskManager()

        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.grid(row=0, column=0, padx=10, pady=10)

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=1, padx=10, pady=10)

        self.task_listbox = tk.Listbox(root, height=10, width=50)
        self.task_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.update_task_listbox()

        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=2, column=0, padx=10, pady=10)

        self.update_button = tk.Button(root, text="Update Task", command=self.update_task)
        self.update_button.grid(row=2, column=1, padx=10, pady=10)

    def update_task_listbox(self):

        self.task_listbox.delete(0, tk.END)
        for task in self.task_manager.tasks:
            self.task_listbox.insert(tk.END, task)

    def add_task(self):

        task = self.task_entry.get()
        if task:
            self.task_manager.add_task(task)
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a task.")

    def delete_task(self):

        selected_task = self.task_listbox.get(tk.ACTIVE)
        if selected_task:
            self.task_manager.remove_task(selected_task)
            self.update_task_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def update_task(self):
        selected_task = self.task_listbox.get(tk.ACTIVE)
        new_task = self.task_entry.get()
        if selected_task and new_task:
            self.task_manager.update_task(selected_task, new_task)
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please select a task and enter a new task description.")


root = tk.Tk()
app = ToDoApp(root)
root.mainloop()
