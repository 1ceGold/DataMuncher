import csv
import os
from datetime import datetime, timedelta

savfil = "todo_list.csv"

# Check file exists
if not os.path.exists(savfil):
    with open(savfil, "w", newline="") as file:
        make_blanc_fil = csv.writer(file)
        make_blanc_fil.writerow(["ID", "Task", "Deadline", "Duration", "Status", "Priority", "Notes"])


# Read file and extract tasks
def init_tasks():
  tasks = []
  with open(savfil, "r") as file:
    extract_from_file = csv.DictReader(file) # saves tasks as dictionary
    #                               slower than lists but more functionality)
    for row in extract_from_file:
      tasks.append(row)
  return tasks

# Save new and unique tasks to file
def save_tasks(tasks):
    with open(savfil, mode="w", newline="") as file:
        save_new_task = csv.writer(file)
        save_new_task.writerow(["ID", "Task", "Deadline", "Duration", "Status", "Priority", "Notes"])
        for task in tasks:
          save_new_task.writerow([task["ID"], task["Task"], task["Deadline"], task["Duration"], task["Status"], task["Priority"], task["Notes"]])
