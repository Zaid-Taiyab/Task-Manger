import os
import json
from datetime import datetime

# File to store tasks
TASKS_FILE = 'tasks.json'

# Function to load tasks from file
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as file:
        tasks = json.load(file)
    return tasks

# Function to save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# Function to add new task
def add_task(tasks):
    task = {}
    task['title'] = input("Enter the task title: ")
    task['category'] = input("Enter the task category: ")
    task['priority'] = input("Enter the task priority (Low, Medium, High): ")
    task['added_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    task['removed_time'] = None
    task['completed'] = False  # New feature: Initialize task as not completed
    tasks.append(task)
    save_tasks(tasks)
    print(f'Task "{task["title"]}" has been added.')

# Function to remove task
def remove_task(tasks):
    task_title = input("Enter the task title to remove: ")
    for task in tasks:
        if task['title'] == task_title and task['removed_time'] is None:
            task['removed_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            added_time = datetime.strptime(task['added_time'], '%Y-%m-%d %H:%M:%S')
            removed_time = datetime.strptime(task['removed_time'], '%Y-%m-%d %H:%M:%S')
            time_diff = removed_time - added_time
            save_tasks(tasks)
            print(f'Task "{task_title}" has been removed. Time in list: {time_diff}')
            return
    print(f'Task "{task_title}" not found or already removed.')

# Function to list all tasks
def list_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return
    sort_by = input("Sort tasks by (category/priority): ").strip().lower()
    if sort_by == 'category':
        tasks = sorted(tasks, key=lambda x: x.get('category', ''))
    elif sort_by == 'priority':
        priority_map = {'Low': 1, 'Medium': 2, 'High': 3}
        tasks = sorted(tasks, key=lambda x: priority_map.get(x.get('priority', 'Low'), 1))
    for i, task in enumerate(tasks, 1):
        added_time = task.get('added_time', 'N/A')
        removed_time = task.get('removed_time', 'N/A')
        completed_status = 'Completed' if task.get('completed', False) else 'Not Completed'
        print(f'{i}. {task["title"]} | Category: {task["category"]} | Priority: {task["priority"]} | Added: {added_time} | Removed: {removed_time} | Status: {completed_status}')

# Function to mark a task as completed
def complete_task(tasks):
    task_title = input("Enter the task title to mark as completed: ")
    for task in tasks:
        if task['title'] == task_title and not task['completed']:
            task['completed'] = True
            save_tasks(tasks)
            print(f'Task "{task_title}" marked as completed.')
            return
    print(f'Task "{task_title}" not found or already completed.')

# Main function 
def main():
    tasks = load_tasks()
    while True:
        print("\nTask Manager")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. List Tasks")
        print("4. Mark Task as Completed")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            remove_task(tasks)
        elif choice == '3':
            list_tasks(tasks)
        elif choice == '4':
            complete_task(tasks)
        elif choice == '5':
            print("Exiting Task Manager.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
