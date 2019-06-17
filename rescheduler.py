import os
import sys
import datetime
from logging import getLogger, StreamHandler, DEBUG
import todoist
from exlist import ExList

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

def missDeadLine(item):
    due = item['due']['date']
    date = due + " 23:59:59"
    due_datetime = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    now = datetime.datetime.now()
    logger.debug(str(item['id']) + ' ' + item['content'])
    logger.debug('due -> ' + date + ', now ->' +  now.strftime("%Y-%m-%d %H:%M:%S"))
    return due_datetime < now

def hasDeadLine(item):
    return item.data['due'] is not None

def reschedule(api, item):
    content = {'string' : item.data['due']['string']}
    item.update(due=None)
    api.commit()
    item.update(due=content)
    api.commit()

def main():
    key = os.getenv("TODOIST_TOKEN")
    if key is None:
        print("Environment Variable named $TODOIST_TOKEN doesn't exist!")
        sys.exit()

    api = todoist.TodoistAPI(key,'https://todoist.com',None,None)
    api.sync()
    items = ExList(api.state['items'])\
            .filter(hasDeadLine)\
            .filter(missDeadLine)
    items.foreach(lambda item: reschedule(api, item))

def exe(event, context):
    main()

if __name__ == '__main__':
    main()
