import argparse

def add_task(args):
    """Handles adding a new task."""
    print(f"Adding task: {args.name} (Duration: {args.duration}h, Deadline: {args.deadline}, Priority: {args.priority})")

def plan_schedule(args):
    """Handles generating an optimized schedule."""
    print("Generating optimized schedule...")

def view_history(args):
    """Handles displaying the task history."""
    print("Displaying task history...")

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

    # Parse arguments and execute the corresponding function
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()