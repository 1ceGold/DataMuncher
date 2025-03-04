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

# Save new and unique tasks to file + ID check
def save_tasks(tasks):
  check_exist_tasks = init_tasks()
  check_exist_id = [int(task["ID"]) for task in check_exist_tasks]


  
  for task in tasks:
    if int(task["ID"]) in check_exist_id: # check for identical IDs to existing tasks
      #                                     Various options, Overwihte, Delete, AUTO ID.
      print(f"\n⚠️ Task with ID {task['ID']} already exists!")
      while True:
        user_mcq = input("Options: (O)verwrite, (G)enerate new ID, (C)ancel: ").strip().lower()

        if user_mcq == "o": # Overwrite
          check_exist_tasks = [t for t in check_exist_tasks if int(t["ID"]) != int(task["ID"])]
          print("✅ Task overwritten.")
          break


        elif user_mcq == "g" # New ID
          new_id = max(check_exist_id) + 1 if check_exist_id else 1
          task["ID"] = new_id
          print(f"✅ New ID generated: {new_id}")
          break

        elif user_mcq == "c": # Cancel
          print("❌ Task not saved.")
          return

        else:
          print("❌ Invalid option. Please try again.")

        # Save all tasks (updated or new) Inefficient as it recreates the whole file and overwrites the original. will come back and rethink this process.
        with open(TODO_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Task", "Deadline", "Duration", "Status", "Priority", "Notes"])
            for task in existing_tasks + [task]:  # Add new/updated task to the list
                writer.writerow([task["ID"], task["Task"], task["Deadline"], task["Duration"], task["Status"], task["Priority"], task["Notes"]])

        print("\n✅ Task saved successfully!")
      # should add return here if i want to add future error checking and save confirmation (eg confirmation email)



def add_task():
  """Add a new task."""
  tasks = init_tasks()

  task_desc = input("Enter the task description: ").strip()

  while True:
      deadl = input("Enter the deadline (YYYY-MM-DD): ").strip()
      try:
          datetime.strptime(deadl, "%Y-%m-%d")
          break
      except ValueError:
          print("Invalid date format. Please use YYYY-MM-DD.")

  while True:
    duration = input("Enter the duration (in hours): ").strip()
    if duration.isdigit():
        break
    else:
        print("Invalid duration. Please enter a valid number.")

  
  priority = input("Enter priority (Low, Medium, High): ").strip().capitalize()
  if priority not in ["Low", "Medium", "High"]:
      print("Invalid priority! Defaulting to 'Medium'.")
      priority = "Medium"

  notes = input("Any additional notes? ").strip()

  new_id = len(tasks) + 1
  tasks.append({"ID": new_id, "Task": task_desc, "Deadline": deadl, "Duration": duration, "Status": "Pending", "Priority": priority, "Notes": notes})
  save_tasks(tasks)
  print("\nTask added successfully!\n")


def display_tasks():
  """Show all tasks sorted by deadline."""
  tasks = sorted(init_tasks(), key=lambda x: x["Deadline"])
  if not tasks:
      print("\nNo tasks found!\n")
      return

  print("\nTo-Do List (Sorted by Deadline):")
  print("-" * 70)
  for task in tasks:
      print(f"{task['ID']}. {task['Task']} | Due: {task['Deadline']} | Status: {task['Status']} | Priority: {task['Priority']} | Notes: {task['Notes']}")
  print("-" * 70)

def delete_task():
  """Delete a task by ID."""
  tasks = init_tasks()
  display_tasks()
  try:
      task_id = int(input("Enter the task ID to delete: "))
      tasks = [task for task in tasks if int(task["ID"]) != task_id]
      save_tasks(tasks)
      print("\nTask deleted successfully!\n")
  except ValueError:
      print("\nInvalid input! Please enter a valid task ID.\n")