import argparse
from tabulate import tabulate
from datetime import datetime
from devtime.scheduler import Task, generate_schedule, WorkSchedule
from devtime.storage import save_tasks, load_tasks, save_schedule, load_schedules

def add_task(args):
    """
    Adds a new task and saves it to storage.

    Args:
        args: Command line arguments containing task details.
    """
    try:
        # Validate and parse the deadline format
        deadline = datetime.strptime(args.deadline, "%Y-%m-%d %H:%M")
        tasks = load_tasks()
        new_task = Task(args.name, args.duration, deadline.strftime("%Y-%m-%d %H:%M"), args.priority)
        tasks.append(new_task)
        save_tasks(tasks)
        print(f"Task added successfully: {new_task}")
    except ValueError:
        print("Error: Invalid date format. Use YYYY-MM-DD HH:MM.")

def plan_schedule(args):
    """
    Generates an optimized schedule based on saved tasks and the work schedule.
    The generated schedule is saved to storage and displayed in a formatted table.

    Args:
        args: Command line arguments.
    """
    tasks = load_tasks()
    schedule = WorkSchedule()
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
    # Assume the ISO datetime contains a 'T' separator and extract the time part.
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
        elif command == "add":
            try:
                name = input("Task name: ")
                duration = float(input("Duration (in hours, e.g., 1.5): "))
                deadline = input("Deadline (YYYY-MM-DD HH:MM): ")
                priority = input("Priority (low, medium, high): ").lower()
                if priority not in ["low", "medium", "high"]:
                    raise ValueError("Invalid priority level.")
                add_task(argparse.Namespace(name=name, duration=duration, deadline=deadline, priority=priority))
            except ValueError as e:
                print(f"⚠ Error: {e}")
        elif command == "plan":
            plan_schedule(None)
        elif command == "schedule":
            view_schedule(None)
        elif command == "history":
            view_history(None)
        elif command in ["edit", "delete", "complete"]:
            print(f"⚠ Command '{command}' is not implemented yet! Coming soon.")
        else:
            print("⚠ Invalid command. Type 'help' to see available commands.")

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

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", required=True)

    # "add" command: Add a new task
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("name", type=str, help="Task name")
    add_parser.add_argument("--duration", type=float, required=True, help="Task duration in hours")
    add_parser.add_argument("--deadline", type=str, required=True, help="Task deadline (YYYY-MM-DD HH:MM)")
    add_parser.add_argument("--priority", type=str, choices=["low", "medium", "high"], default="medium", help="Task priority")
    add_parser.set_defaults(func=add_task)

    # "plan" command: Generate an optimized schedule
    plan_parser = subparsers.add_parser("plan", help="Generate optimized schedule")
    plan_parser.set_defaults(func=plan_schedule)

    # "history" command: View task history
    history_parser = subparsers.add_parser("history", help="View task history")
    history_parser.set_defaults(func=view_history)

    # "schedule" command: View last saved schedule
    schedule_parser = subparsers.add_parser("schedule", help="View last saved schedule")
    schedule_parser.set_defaults(func=view_schedule)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()