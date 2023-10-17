import json
import time
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return None
        send_slack_notification(f"A file was created: {event.src_path}")
    def on_deleted(self, event):
        if event.is_directory:
            return None
        send_slack_notification(f"A file was deleted: {event.src_path}")
    def on_moved(self, event):
        if event.is_directory:
            return None
        send_slack_notification(f"A file was moved from {event.src_path} to {event.dest_path}")
def send_slack_notification(message):
    webhook_url = "<enter URL here>"
    headers = {'content-type': 'application/json'}
    data = {'text': message}
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print(f"Sent slack notification: {message}")
    else:
        print(f"Failed sending slack notification: {response.status_code} - {response.text}")
if __name__ == "__main__":
    path = "/home/ec2-user/myDir/"
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
