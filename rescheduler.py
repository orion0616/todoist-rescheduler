import os
import sys
import datetime

from todoist.api import TodoistAPI
from exlist import ExList

def missDeadLine(item):
    due = item['due_date_utc']
    due_datetime = datetime.datetime.strptime(due, "%a %d %b %Y %H:%M:%S %z")
    now = datetime.datetime.now(datetime.timezone.utc)
    return due_datetime < now

def hasDeadLine(item):
    return item['date_string'] is not None

def makeProjectMap(api):
    projects = ExList(api.state['projects']).map(lambda p: (p['id'], p['name']))
    return dict(projects)

def resche1DayTask(api, item):
    now = datetime.datetime.utcnow()
    due = now + datetime.timedelta(hours=9)
    due = due.strftime('%-m月%-d日')
    item.update(date_string= due +'から毎日')

def main():
    key = os.getenv("TODOIST_TOKEN")
    if key is None:
        print("Environment Variable named $TODOIST_TOKEN doesn't exist!")
        sys.exit()

    api = TodoistAPI(key, cache=None)
    api.sync()
    items = ExList(api.state['items'])\
            .filter(hasDeadLine)\
            .filter(missDeadLine)
    projectMap = makeProjectMap(api)

    # For 1day routine
    items.filter(lambda i: projectMap[i['project_id']] == '1Day Routine')\
            .foreach(lambda i: resche1DayTask(api, i))
    api.commit()

def exe(event, context):
    main()

if __name__ == '__main__':
    main()
