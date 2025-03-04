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

# Pure save function
def save_tasks(tasks):
  with open(savfil, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["ID", "Task", "Deadline", "Duration", "Status", "Priority", "Notes"])
    for task in tasks:
        writer.writerow([task["ID"], task["Task"], task["Deadline"], task["Duration"], task["Status"], task["Priority"], task["Notes"]])


# Removed ID handling from user via Auto ID in add_task
def add_task():
  tasks = init_tasks()

  while True:

    
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


  # Task Preview
    print("\n📌 **Task Preview**")
    print(f"   Task: {task_desc}")
    print(f"   Deadline: {deadl}")
    print(f"   Duration: {duration} hours")
    print(f"   Priority: {priority}")
    print(f"   Notes: {notes}")

    user_in = input("Choose an option: ").strip().lower()
  
    if user_in == "t":
        break  # Go back to task description input
    elif user_in == "d":
        continue  # Restart to edit deadline
    elif user_in == "h":
        continue  # Restart to edit duration
    elif user_in == "p":
        continue  # Restart to edit priority
    elif user_in == "n":
        continue  # Restart to edit notes
    elif user_in == "c":
        break  # Confirm and move forward
    elif user_in == "x":
        print("\n❌ Task creation cancelled.")
        return  # Exit without saving
    else:
        print("❌ Invalid option! Please choose again.")

  #  """ new_id = len(tasks) + 1 """ # Deleted tasks will not allow their ID to be reused with this line. new logic neeeded

  #  New system works by storing all IDs as a set of ints from 1 to n + 1. this ensures all IDs that have been used before are listed with the addition of a new ID incase they are all in use. All the theoretical IDs are then subtracted against the set of used IDs. this leave an ordered list of unused IDs of which the lowest int ID is used ensuring effient use of IDs.
  existing_ids = {int(task["ID"]) for task in tasks} if tasks else set()
  if existing_ids:
    all_possible_ids = set(range(1, max(existing_ids) + 2))
    available_ids = sorted(all_possible_ids - existing_ids)
    new_id = available_ids[0]
  else:
    new_id = 1

  tasks.append({"ID": new_id, "Task": task_desc, "Deadline": deadl, "Duration": duration, "Status": "Pending", "Priority": priority, "Notes": notes})
  save_tasks(tasks)
  print("\nTask added successfully!\n")


def display_tasks():
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
  tasks = init_tasks()
  display_tasks()
  try:
      task_id = int(input("Enter the task ID to delete: "))
      tasks = [task for task in tasks if int(task["ID"]) != task_id]
      save_tasks(tasks)
      print("\nTask deleted successfully!\n")
  except ValueError:
      print("\nInvalid input! Please enter a valid task ID.\n")





def mark_task_completed():
  """Mark a task as completed."""
  tasks = load_tasks()
  display_tasks()
  try:
      task_id = int(input("Enter the task ID to mark as completed: "))
      for task in tasks:
          if int(task["ID"]) == task_id:
              task["Status"] = "Completed"
              break
      save_tasks(tasks)
      print("\nTask marked as completed!\n")
  except ValueError:
      print("\nInvalid input! Please enter a valid task ID.\n")

def edit_task():
  """Edit task details (priority, notes, etc.)."""
  tasks = init_tasks()
  display_tasks()

  try:
      task_id = int(input("Enter the task ID to edit: "))
      for task in tasks:
          if int(task["ID"]) == task_id:
              print(f"Editing Task: {task['Task']}")
              task["Priority"] = input(f"Enter new priority (Low, Medium, High) [{task['Priority']}]: ").strip().capitalize() or task["Priority"]
              task["Notes"] = input(f"Enter new notes [{task['Notes']}]: ").strip() or task["Notes"]
              save_tasks(tasks)
              print("\nTask updated successfully!\n")
              return
      print("\nTask not found!\n")
  except ValueError:
      print("\nInvalid input! Please enter a valid task ID.\n")

def show_calendar():
  """Display tasks due in the next 7 days."""
  tasks = init_tasks()
  today = datetime.today()
  upcoming_tasks = [task for task in tasks if datetime.strptime(task["Deadline"], "%Y-%m-%d") <= (today + timedelta(days=7))]

  print("\n📅 Upcoming Tasks (Next 7 Days):")
  print("-" * 70)
  if upcoming_tasks:
      for task in upcoming_tasks:
          print(f"{task['ID']}. {task['Task']} | Due: {task['Deadline']} | Status: {task['Status']} | Priority: {task['Priority']} | Notes: {task['Notes']}")
  else:
      print("No tasks due in the next 7 days.")
  print("-" * 70)

def main():
  """Main function to navigate through different modes."""
  while True:
      print("\nOptions:")
      print("1 - View To-Do List")
      print("2 - Add a New Task")
      print("3 - Delete a Task")
      print("4 - Mark Task as Completed")
      print("5 - Edit Task")
      print("6 - Show Calendar (Next 7 Days)")
      print("7 - Exit")

      choice = input("\nEnter your choice: ").strip()

      if choice == "1":
          display_tasks()
      elif choice == "2":
          add_task()
      elif choice == "3":
          delete_task()
      elif choice == "4":
          mark_task_completed()
      elif choice == "5":
          edit_task()
      elif choice == "6":
          show_calendar()
      elif choice == "7":
          print("\nGoodbye!")
          break
      else:
          print("\nInvalid choice! Please enter a number from 1 to 7.")

if __name__ == "__main__":
  main()