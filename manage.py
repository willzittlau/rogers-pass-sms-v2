# from flask_script import Manager
# from app import app
# from sms import send_update
# from status import get_status
# from app import time

# manager = Manager(app)

# @manager.command
# def sms():
#     time.sleep(300)
#     send_update()

# @manager.command
# def scrape():
#     time.sleep(240)
#     get_status()

# @manager.command
# def both():
#     time.sleep(240)
#     get_status()
#     time.sleep(60)
#     send_update()

# if __name__ == "__main__":
#     manager.run()