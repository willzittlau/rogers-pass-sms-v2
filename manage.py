from flask_script import Manager
from app import app
from sms import send_update
from status import get_status
import time

manager = Manager(app)

@manager.command
def both():
  # Free tier scheduler only has hourly CRON tasks, this will ensure SMS is sent at 7:05 AM
    time.sleep(300)
    send_update()

if __name__ == "__main__":
    manager.run()