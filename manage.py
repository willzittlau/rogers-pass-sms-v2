from flask_script import Manager
from app import app
from sms import send_update
from status import get_status
import time

manager = Manager(app)

@manager.command
def both():
  # Free tier scheduler only has hourly CRON tasks, this will ensure SMS is sent at 7:15 AM
    time.sleep(840)
    get_status()
    time.sleep(60)
    send_update()

if __name__ == "__main__":
    manager.run()