# cli_tool.py

import argparse
import sys

# Handle both direct execution and module execution
try:
    from .models import Task, User
except ImportError:
    from models import Task, User

# Global dictionary to store users and their tasks
users = {}

def add_task(args):
    # Check if the user exists, if not, create one
    user = users.get(args.user)
    if not user:
        user = User(args.user)
        users[args.user] = user
    
    # Create a new Task with the given title
    task = Task(args.title)
    
    # Add the task to the user's task list
    user.add_task(task)

def complete_task(args):
    # Look up the user by name
    user = users.get(args.user)
    if not user:
        print("❌ User not found.")
        return
    
    # Look up the task by title
    task = user.get_task_by_title(args.title)
    if not task:
        print("❌ Task not found.")
        return
    
    # Mark the task as complete
    task.complete()

def list_tasks(args):
    """List all tasks for a specific user"""
    user = users.get(args.user)
    if not user:
        print("❌ User not found.")
        return
    
    if not user.tasks:
        print(f"📝 {user.name} has no tasks.")
        return
    
    print(f"📋 Tasks for {user.name}:")
    for i, task in enumerate(user.tasks, 1):
        status = "✅" if task.completed else "⏳"
        print(f"  {i}. {status} {task.title}")

def main():
    parser = argparse.ArgumentParser(
        description="Task Manager CLI - Manage tasks for users",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli_tool.py add-task Alice "Write unit tests"
  python cli_tool.py complete-task Alice "Write unit tests"
  python cli_tool.py list-tasks Alice
        """
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Subparser for adding tasks
    add_parser = subparsers.add_parser("add-task", help="Add a task for a user")
    add_parser.add_argument("user", help="Username to add task for")
    add_parser.add_argument("title", help="Task title")
    add_parser.set_defaults(func=add_task)

    # Subparser for completing tasks
    complete_parser = subparsers.add_parser("complete-task", help="Complete a user's task")
    complete_parser.add_argument("user", help="Username")
    complete_parser.add_argument("title", help="Task title to complete")
    complete_parser.set_defaults(func=complete_task)

    # Subparser for listing tasks
    list_parser = subparsers.add_parser("list-tasks", help="List all tasks for a user")
    list_parser.add_argument("user", help="Username to list tasks for")
    list_parser.set_defaults(func=list_tasks)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
