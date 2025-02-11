import argparse
import shlex
from tabulate import tabulate
from datetime import datetime

from devtime.scheduler import Task, generate_schedule, WorkSchedule
from devtime.storage import (
    generate_task_id, save_tasks, load_tasks, save_schedule, load_schedules, 
    load_completed_tasks, save_completed_tasks
)
from devtime.config import load_config, save_config, update_config

def parse_date(date_str):
    """
    Parses various date formats into a full datetime object.

    Args:
        date_str (str or datetime): The input date string or datetime object.

    Returns:
        datetime or None: The parsed datetime object or None if no deadline.

    Raises:
        ValueError: If the date format is invalid.
    """
    now = datetime.now()

    if isinstance(date_str, datetime):
        return date_str

    if date_str is None or date_str.strip() == "" or date_str.strip().lower() == "none":
        return None

    date_str = date_str.strip()

    if date_str.isdigit():
        full_date = f"{now.year}-{now.month:02d}-{int(date_str):02d}"
        time_part = "23:59" 

    elif ":" in date_str and "-" not in date_str and " " not in date_str:
        full_date = now.strftime("%Y-%m-%d")
        time_part = date_str

    elif " " in date_str and date_str.split(" ")[0].isdigit():
        day_part, time_part = date_str.split(" ", 1)
        full_date = f"{now.year}-{now.month:02d}-{int(day_part):02d}"

    elif "-" in date_str:
        parts = date_str.split(" ")
        full_date = parse_date_part(parts[0], now)
        time_part = parts[1] if len(parts) > 1 else "23:59"

    else:
        raise ValueError(f"Invalid date format: '{date_str}'. Expected formats: '10', '02-10', 'YYYY-MM-DD [HH:MM]', or 'HH:MM'.")

    try:
        return datetime.strptime(f"{full_date} {time_part}", "%Y-%m-%d %H:%M")
    except ValueError as e:
        raise ValueError(f"Invalid date format: '{date_str}'. Expected formats: '10', '02-10', 'YYYY-MM-DD [HH:MM]', or 'HH:MM'. Error: {e}")

def parse_date_part(date_part, now):
    """
    Parses different formats of the date part.

    Args:
        date_part (str): The date part of the input string.
        now (datetime): The current datetime.

    Returns:
        str: The parsed date part in 'YYYY-MM-DD' format.
    """
    if "-" not in date_part:  
        if len(date_part) <= 2:  
            return f"{now.year}-{now.month:02d}-{int(date_part):02d}"
        else:
            raise ValueError(f"Invalid date format: '{date_part}'. Expected 'MM-DD' or 'YYYY-MM-DD'.")
    
    elif date_part.count("-") == 1:
        return f"{now.year}-{date_part}"
    
    return date_part

def parse_priority(priority_input):
    """
    Parses priority input (either number or text).

    Args:
        priority_input (str or int): The priority input.

    Returns:
        str: The parsed priority ('high', 'medium', or 'low').
    """
    priority_map = {"1": "high", "2": "medium", "3": "low", "high": "high", "medium": "medium", "low": "low"}
    return priority_map.get(str(priority_input).lower(), "medium")

def parse_add_args(args):
    """
    Parses and corrects the format of the add command arguments.

    Args:
        args (list[str]): List of arguments passed in the command.

    Returns:
        dict: Corrected arguments.
    """
    name = args[0]
    duration = args[1]
    deadline = None
    priority = "2"  # Default value (medium)

    if len(args) > 2:
        if len(args) > 3 and ":" in args[3]: 
            deadline = f"{args[2]} {args[3]}"
            priority = args[4] if len(args) > 4 else priority
        else: 
            deadline = args[2]
            priority = args[3] if len(args) > 3 else priority

    return argparse.Namespace(
        name=name,
        duration=duration,
        deadline=deadline,
        priority=priority
    )

def add_task(args):
    """
    Handles adding a new task and saving it to storage.
    """
    tasks = load_tasks()
    task_id = generate_task_id()

    name = args.name
    duration = float(args.duration)
    deadline = parse_date(args.deadline) if args.deadline else None
    priority = parse_priority(args.priority)

    new_task = Task(name, duration, deadline, priority, task_id)
    tasks.append(new_task)
    save_tasks(tasks)

    print(f"✅ Task added: [ID {task_id}] {new_task.name}, {new_task.duration}h, "
          f"{new_task.deadline.strftime('%Y-%m-%d %H:%M') if new_task.deadline else 'No deadline'}, {new_task.priority}")

def delete_task(args):
    """
    Deletes tasks by their IDs from active or completed lists. Supports "all" to delete all completed tasks.

    Args:
        args (Namespace): Command-line arguments containing task IDs and optional --completed flag.
    """
    tasks = load_tasks()
    completed_tasks = load_completed_tasks()

    # Convert IDs to integers (if not "all")
    active_ids = list(map(int, args.active_ids)) if args.active_ids else []
    completed_ids = [] if args.completed_ids is None else args.completed_ids

    # Delete from active tasks
    if active_ids:
        initial_count = len(tasks)
        tasks = [task for task in tasks if task.id not in active_ids]
        if len(tasks) < initial_count:
            save_tasks(tasks)
            print(f"✅ Deleted active tasks: {', '.join(map(str, active_ids))}.")
        else:
            print(f"⚠ No matching active tasks found for IDs: {', '.join(map(str, active_ids))}.")

    # Delete from completed tasks
    if "all" in completed_ids:
        confirm = input("⚠ Are you sure you want to delete all completed tasks? (yes/no): ").strip().lower()
        if confirm == "yes" or confirm == "y":
            save_completed_tasks([])
            print("✅ All completed tasks have been deleted.")
        else:
            print("🚫 Operation canceled.")
        return

    if completed_ids:
        completed_ids = list(map(int, completed_ids))
        initial_count = len(completed_tasks)
        completed_tasks = [task for task in completed_tasks if task.id not in completed_ids]
        if len(completed_tasks) < initial_count:
            save_completed_tasks(completed_tasks)
            print(f"✅ Deleted completed tasks: {', '.join(map(str, completed_ids))}.")
        else:
            print(f"⚠ No matching completed tasks found for IDs: {', '.join(map(str, completed_ids))}.")

def edit_task(args):
    """
    Edits an existing task based on user input.

    Args:
        args (Namespace): Command-line arguments containing task ID and new values.
    """
    tasks = load_tasks()
    task_id = args.id

    for task in tasks:
        if task.id == task_id:
            if args.name:
                task.name = args.name
            if args.duration:
                task.duration = args.duration
            if args.deadline:
                task.deadline = datetime.strptime(args.deadline, "%Y-%m-%d %H:%M")
            if args.priority:
                task.priority = args.priority

            save_tasks(tasks)
            print(f"✅ Task {task_id} updated successfully.")
            return

    print(f"⚠ Task with ID {task_id} not found.")

def complete_task(args):
    """
    Marks one or multiple tasks as completed. Supports "all" to complete all tasks.

    Args:
        args (Namespace): Command-line arguments containing task IDs or "all".
    """
    tasks = load_tasks()
    completed_tasks = load_completed_tasks()

    if "all" in args.ids:
        confirm = input("⚠ Are you sure you want to mark all tasks as completed? (yes/no): ").strip().lower()
        if confirm == "yes" or "y":
            completed_tasks.extend(tasks)
            save_completed_tasks(completed_tasks)
            save_tasks([])
            print("✅ All tasks have been marked as completed.")
        else:
            print("🚫 Operation canceled.")
        return

    initial_count = len(tasks)
    remaining_tasks = [task for task in tasks if task.id not in map(int, args.ids)]
    completed_now = [task for task in tasks if task.id in map(int, args.ids)]

    if not completed_now:
        print(f"⚠ No matching tasks found for IDs: {', '.join(args.ids)}.")
    else:
        completed_tasks.extend(completed_now)
        save_completed_tasks(completed_tasks)
        save_tasks(remaining_tasks)
        print(f"✅ Successfully marked tasks as completed: {', '.join(args.ids)}.")

def plan_schedule(args):
    """
    Generates an optimized schedule based on saved tasks and the work schedule.
    The generated schedule is saved to storage and displayed in a formatted table.

    Args:
        args: Command line arguments.
    """
    tasks = load_tasks()
    today = datetime.today().strftime("%A")
    schedule = WorkSchedule(today)
    planned_tasks, remaining_tasks = generate_schedule(tasks, schedule)

    # Save the generated schedule with the current date
    schedule_date = datetime.now()
    save_schedule(schedule_date, planned_tasks)

    if planned_tasks:
        headers = ["Task Name", "Duration", "Deadline"]
        table_data = [
            [task.name, f"{task.duration}h", task.deadline.strftime("%H:%M")] for task in planned_tasks
        ]
        print("\n┌──────────────────────────────────────────┐")
        print("│            OPTIMIZED SCHEDULE            │")
        print("└──────────────────────────────────────────┘\n")
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    else:
        print("\n📅 No tasks scheduled for today.")

    if remaining_tasks:
        print("\n⚠ Some tasks couldn't fit into today’s schedule and will be postponed:")
        for task in remaining_tasks:
            print(f"- {task.name} ({task.duration}h, deadline: {task.deadline.strftime('%Y-%m-%d %H:%M')}, priority: {task.priority})")

def view_history(args):
    """
    Displays the task history.

    Args:
        args: Command line arguments.
    """
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
    else:
        print("Task History:")
        for task in tasks:
            print(task)

def view_schedule(args):
    """
    Displays the last saved schedule.

    Args:
        args: Command line arguments.
    """
    schedules = load_schedules()
    
    if not schedules:
        print("⚠ No saved schedules found.")
        return

    # Display the most recent schedule
    last_schedule = schedules[-1]
    print(f"\n📅 Schedule for {last_schedule['date']}:")
    table = [
        [task["name"], f"{task['duration']}h", task["deadline"].split("T")[1]] 
        for task in last_schedule["tasks"]
    ]
    print(tabulate(table, headers=["Task Name", "Duration", "Deadline"], tablefmt="grid"))

def interactive_mode():
    """Runs the interactive CLI mode, allowing users to enter commands in a loop."""
    
    print("\nWelcome to DevTime interactive mode!")
    print("Type a command or 'help' to see available commands.")
    print("-" * 50)

    while True:
        command = input("DevTime> ").strip().lower()

        if command in ["q", "exit", "quit"]:
            print("Exiting interactive mode. Goodbye!")
            break
        elif command == "help":
            print("\nAvailable commands:")
            print("  add        - Add a new task")
            print("  plan       - Generate an optimized schedule")
            print("  schedule   - View the last saved schedule")
            print("  history    - View task history")
            print("  edit       - Edit an existing task")
            print("  delete     - Delete a task")
            print("  complete   - Mark a task as completed")
            print("  exit       - Exit interactive mode")
            print("-" * 50)
        elif command.startswith("add"):
            try:
                parts = shlex.split(command)
                args = parts[1:]

                name = args[0] if len(args) > 0 else input("Task name: ").strip()
                duration = args[1] if len(args) > 1 else input("Duration (in hours, e.g., 1.5): ").strip()
                deadline = args[2] if len(args) > 2 else input("Deadline (YYYY-MM-DD HH:MM, leave empty for none): ").strip()
                priority = args[3] if len(args) > 3 else input("Priority (1=high, 2=medium, 3=low, leave empty for medium): ").strip()

                duration = float(duration)
                deadline = parse_date(deadline) if deadline else None
                priority_map = {"1": "high", "2": "medium", "3": "low", "high": "high", "medium": "medium", "low": "low"}
                priority = priority_map.get(priority, "medium")

                add_task(argparse.Namespace(name=name, duration=duration, deadline=deadline, priority=priority))

            except ValueError as e:
                print(f"⚠ Error: {e}")
        elif command == "edit":
            task_id = int(input("Task ID: ").strip())
            name = input("New name (leave empty to keep current): ").strip()
            duration = input("New duration (leave empty to keep current): ").strip()
            deadline = input("New deadline (YYYY-MM-DD HH:MM, leave empty to keep current): ").strip()
            priority = input("New priority (1=high, 2=medium, 3=low, leave empty to keep current): ").strip().lower()

            priority_map = {"1": "high", "2": "medium", "3": "low", "high": "high", "medium": "medium", "low": "low"}
            priority = priority_map.get(priority, None)

            edit_task(argparse.Namespace(
                id=task_id,
                name=name or None,
                duration=float(duration) if duration else None,
                deadline=deadline or None,
                priority=priority
            ))

        elif command.startswith("delete"):
            parts = command.split()
            
            if len(parts) > 1:
                try:
                    task_id = int(parts[1])
                    delete_task(argparse.Namespace(id=task_id))
                except ValueError:
                    print("⚠ Invalid task ID. Please enter a number.")
            else:
                try:
                    task_id = int(input("Task ID: ").strip())
                    delete_task(argparse.Namespace(id=task_id))
                except ValueError:
                    print("⚠ Invalid task ID. Please enter a number.")
        elif command == "complete":
            task_id = int(input("Task ID: ").strip())
            complete_task(argparse.Namespace(id=task_id))
        elif command == "plan":
            plan_schedule(None)
        elif command == "schedule":
            view_schedule(None)
        elif command == "history":
            view_history(None)
        else:
            print("⚠ Invalid command. Type 'help' to see available commands.")

def view_config(args):
    """Displays the current user configuration."""
    config = load_config()
    print("\n🔧 User Configuration:")
    for key, value in config.items():
        print(f"{key}: {value}")

def update_work_hours(args):
    """Updates working hours for a specific day."""
    config = load_config()
    
    if args.start.lower() == "none":
        config["work_hours"][args.day] = {"start": None, "end": None}
    else:
        config["work_hours"][args.day] = {"start": int(args.start), "end": int(args.end)}
    
    save_config(config)
    print(f"✅ Updated working hours for {args.day}.")

def update_concentration(args):
    """Updates max concentration hours."""
    update_config("max_concentration_hours", float(args.hours))
    print(f"✅ Updated max concentration hours to {args.hours}h.")

def update_break(args):
    """Updates minimum break time."""
    update_config("min_break_minutes", int(args.minutes))
    print(f"✅ Updated minimum break to {args.minutes} minutes.")

def main():
    """
    Sets up the CLI interface using argparse and executes the corresponding command.
    If no command is provided, launches interactive mode.
    """
    import sys

    if len(sys.argv) == 1:
        interactive_mode()
        return

    parser = argparse.ArgumentParser(
        prog="DevTime",
        description="Intelligent CLI-based task scheduler for developers."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # "add" command: Add a new task
    add_parser = subparsers.add_parser("add", help="Add a new task with flexible input")
    add_parser.add_argument("name", type=str, help="Task name (use quotes for multiple words)")
    add_parser.add_argument("duration", type=float, help="Task duration in hours")
    add_parser.add_argument("deadline", type=str, nargs="*", default=None, help="Deadline (e.g. '10', '02-10', '2025-02-10 18:00')")
    add_parser.add_argument("priority", type=str, nargs="?", default="2", help="Priority (1=high, 2=medium, 3=low or 'high')")
    add_parser.set_defaults(func=add_task)

    # "delete" command: Delete a task
    delete_parser = subparsers.add_parser("delete", help="Delete tasks from active or completed lists.")
    delete_parser.add_argument("active_ids", nargs="*", help="Task IDs to delete from active tasks.")
    delete_parser.add_argument("--completed", nargs="*", dest="completed_ids", help="Task IDs to delete from completed tasks.")
    delete_parser.set_defaults(func=delete_task)

    # "edit" command: Edit an existing task
    edit_parser = subparsers.add_parser("edit", help="Edit a task")
    edit_parser.add_argument("id", type=int, help="Task ID")
    edit_parser.add_argument("--name", type=str, help="New task name", required=False)
    edit_parser.add_argument("--duration", type=float, help="New task duration in hours", required=False)
    edit_parser.add_argument("--deadline", type=str, help="New deadline (YYYY-MM-DD HH:MM)", required=False)
    edit_parser.add_argument("--priority", type=str, choices=["low", "medium", "high"], help="New task priority", required=False)
    edit_parser.set_defaults(func=edit_task)

    # "complete" command: Mark a task as completed
    complete_parser = subparsers.add_parser("complete", help="Mark tasks as completed.")
    complete_parser.add_argument("ids", nargs="+", help="Task IDs to mark as completed or 'all' to complete all tasks.")
    complete_parser.set_defaults(func=complete_task)

    # "plan" command: Generate an optimized schedule
    plan_parser = subparsers.add_parser("plan", help="Generate optimized schedule")
    plan_parser.set_defaults(func=plan_schedule)

    # "history" command: View task history
    history_parser = subparsers.add_parser("history", help="View task history")
    history_parser.set_defaults(func=view_history)

    # "schedule" command: View last saved schedule
    schedule_parser = subparsers.add_parser("schedule", help="View last saved schedule")
    schedule_parser.set_defaults(func=view_schedule)

    # "config" command: View or change user settings
    config_parser = subparsers.add_parser("config", help="View or change user settings")
    config_parser.set_defaults(func=view_config)

    # Subparsers for configuration commands
    work_hours_parser = subparsers.add_parser("config-hours", help="Update working hours")
    work_hours_parser.add_argument("day", type=str, help="Day of the week")
    work_hours_parser.add_argument("start", type=str, help="Start time (or 'none' to set as a day off)")
    work_hours_parser.add_argument("end", type=str, help="End time (ignored if 'none')")
    work_hours_parser.set_defaults(func=update_work_hours)

    # Subparsers for updating concentration and break time
    concentration_parser = subparsers.add_parser("config-focus", help="Update concentration time")
    concentration_parser.add_argument("hours", type=float, help="Max concentration hours")
    concentration_parser.set_defaults(func=update_concentration)

    # "config-break" command: Update minimum break time
    break_parser = subparsers.add_parser("config-break", help="Update break time")
    break_parser.add_argument("minutes", type=int, help="Minimum break time in minutes")
    break_parser.set_defaults(func=update_break)

    args = parser.parse_args()

    if args.command == "add":

        deadline = None
        priority = args.priority 

        if isinstance(args.deadline, list):
            args.deadline = [d.strip() for d in args.deadline if d.strip()] 

        if args.deadline:
            if len(args.deadline) == 1: 
                deadline = args.deadline[0]
            elif len(args.deadline) == 2 and " " not in args.deadline[0]:
                if ":" in args.deadline[1]:
                    deadline = f"{args.deadline[0]} {args.deadline[1]}"
                else:
                    deadline = f"{args.deadline[0]}"
                    priority = args.deadline[1]
            elif len(args.deadline) == 2 and " " in args.deadline[0]: 
                deadline = f"{args.deadline[0]}"
                priority = args.deadline[1]
            elif len(args.deadline) > 2:  
                deadline = f"{args.deadline[0]} {args.deadline[1]}"
                priority = args.deadline[2] 

        if not deadline:
            deadline = None

        valid_priorities = {"1": "high", "2": "medium", "3": "low"}
        priority = valid_priorities.get(priority, "medium")

        args = argparse.Namespace(
            name=args.name,
            duration=args.duration,
            deadline=deadline,
            priority=priority,
            func=add_task
        )

    args.func(args)

if __name__ == "__main__":
    main()