import datetime
import os
import sys
from todoist_api_python.api import TodoistAPI

def has_recurring_deadline(task):
    if task.due is None:
        return False
    return task.due.is_recurring

def is_after_deadline(task):
    due = task.due.date
    date = due + " 23:59:59"
    due_datetime = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    now = datetime.datetime.now()
    return due_datetime < now

def get_tasks(api):
    try:
        tasks = api.get_tasks()
        print(str(len(tasks)) + " tasks are gotten.")
    except Exception as error:
        print(error)
    return tasks

def reschedule_task(task, api):
    due = task.due.string
    api.update_task(task_id = task.id, due_string=due)

def main():
    token = os.getenv("TODOIST_TOKEN")
    if token is None:
        print("Environment Variable named $TODOIST_TOKEN doesn't exist!")
        sys.exit()
    api = TodoistAPI(token)
    tasks = get_tasks(api)
    for task in tasks:
        if has_recurring_deadline(task) and is_after_deadline(task):
            reschedule_task(task, api)


def exe(event, context):
    main()

if __name__ == "__main__":
    main()
