import argparse
from tabulate import tabulate
from datetime import datetime
from devtime.scheduler import Task, generate_schedule, WorkSchedule
from devtime.storage import save_tasks, load_tasks, save_schedule, load_schedules

def add_task(args):
    """Handles adding a new task and saving it to storage."""
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
    """Handles generating an optimized schedule."""
    tasks = load_tasks()
    schedule = WorkSchedule()
    planned_tasks, remaining_tasks = generate_schedule(tasks, schedule)

    # Save the generated schedule
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
    """Handles displaying the task history."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
    else:
        print("Task History:")
        for task in tasks:
            print(task)

def view_schedule(args):
    """Handles displaying saved schedules."""
    schedules = load_schedules()
    
    if not schedules:
        print("⚠ No saved schedules found.")
        return

    # Виводимо останній розклад
    last_schedule = schedules[-1]
    print(f"\n📅 Schedule for {last_schedule['date']}:")
    table = [[task["name"], f"{task['duration']}h", task["deadline"].split("T")[1]] for task in last_schedule["tasks"]]
    print(tabulate(table, headers=["Task Name", "Duration", "Deadline"], tablefmt="grid"))

def main():
    """Main function to set up the CLI interface using argparse."""
    parser = argparse.ArgumentParser(
        prog="DevTime",
        description="Intelligent CLI-based task scheduler for developers."
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", required=True)

    # "add" command: Add a new task
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("name", type=str, help="Task name")
    add_parser.add_argument("--duration", type=int, required=True, help="Task duration in hours")
    add_parser.add_argument("--deadline", type=str, required=True, help="Task deadline (YYYY-MM-DD HH:MM)")
    add_parser.add_argument("--priority", type=str, choices=["low", "medium", "high"], default="medium", help="Task priority")
    add_parser.set_defaults(func=add_task)

    # "plan" command: Generate a task schedule
    plan_parser = subparsers.add_parser("plan", help="Generate optimized schedule")
    plan_parser.set_defaults(func=plan_schedule)

    # "history" command: View past tasks
    history_parser = subparsers.add_parser("history", help="View task history")
    history_parser.set_defaults(func=view_history)

    schedule_parser = subparsers.add_parser("schedule", help="View last saved schedule")
    schedule_parser.set_defaults(func=view_schedule)

    # Parse arguments and execute the corresponding function
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()