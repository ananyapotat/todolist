import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime, date

class Task:
    def __init__(self, description, due_date=None, priority=None, category=None):
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.category = category

    def to_dict(self):
        return {
            'description': self.description,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'priority': self.priority,
            'category': self.category
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(data['description'])
        task.due_date = date.fromisoformat(data['due_date']) if data['due_date'] else None
        task.priority = data['priority']
        task.category = data['category']
        return task

class ToDoListApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List Application")
        self.master.geometry("800x600")  # Increased window size

        self.tasks = []
        self.load_tasks()

        self.create_widgets()

    def create_widgets(self):
        # Create a main frame
        main_frame = tk.Frame(self.master)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Input frame
        input_frame = tk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))

        # Task input
        tk.Label(input_frame, text="Task:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.task_entry = tk.Entry(input_frame, width=40)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        # Due date input
        tk.Label(input_frame, text="Due Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.due_date_entry = tk.Entry(input_frame, width=40)
        self.due_date_entry.grid(row=1, column=1, padx=5, pady=5)

        # Priority input
        tk.Label(input_frame, text="Priority:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.priority_var = tk.StringVar(self.master)
        self.priority_var.set("Medium")
        priority_options = ["Low", "Medium", "High"]
        self.priority_menu = tk.OptionMenu(input_frame, self.priority_var, *priority_options)
        self.priority_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Category input
        tk.Label(input_frame, text="Category:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.category_entry = tk.Entry(input_frame, width=40)
        self.category_entry.grid(row=3, column=1, padx=5, pady=5)

        # Task list
        self.task_list = ttk.Treeview(main_frame, columns=("Description", "Due Date", "Priority", "Category"), show="headings")
        self.task_list.heading("Description", text="Description")
        self.task_list.heading("Due Date", text="Due Date")
        self.task_list.heading("Priority", text="Priority")
        self.task_list.heading("Category", text="Category")
        self.task_list.pack(fill=tk.BOTH, expand=True)

        # Scrollbar for task list
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.task_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.task_list.configure(yscrollcommand=scrollbar.set)

        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        # Add task button
        self.add_button = tk.Button(button_frame, text="Add Task", command=self.add_task, width=15)
        self.add_button.pack(side=tk.LEFT, padx=(0, 5))

        # Remove task button
        self.remove_button = tk.Button(button_frame, text="Remove Task", command=self.remove_task, width=15)
        self.remove_button.pack(side=tk.LEFT)

        self.update_task_list()

    def add_task(self):
        description = self.task_entry.get()
        due_date_str = self.due_date_entry.get()
        priority = self.priority_var.get()
        category = self.category_entry.get()

        if not description:
            messagebox.showerror("Error", "Task description cannot be empty!")
            return

        try:
            due_date = date.fromisoformat(due_date_str) if due_date_str else None
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        task = Task(description, due_date, priority, category)
        self.tasks.append(task)
        self.update_task_list()
        self.save_tasks()
        self.clear_inputs()

    def remove_task(self):
        selected_item = self.task_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a task to remove.")
            return

        index = self.task_list.index(selected_item)
        del self.tasks[index]
        self.update_task_list()
        self.save_tasks()

    def update_task_list(self):
        self.task_list.delete(*self.task_list.get_children())
        for task in self.tasks:
            due_date = task.due_date.isoformat() if task.due_date else ""
            self.task_list.insert("", "end", values=(task.description, due_date, task.priority, task.category))

    def clear_inputs(self):
        self.task_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
        self.priority_var.set("Medium")
        self.category_entry.delete(0, tk.END)

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                task_data = json.load(f)
                self.tasks = [Task.from_dict(data) for data in task_data]
        except FileNotFoundError:
            self.tasks = []

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()