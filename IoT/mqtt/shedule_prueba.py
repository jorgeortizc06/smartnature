import schedule
import time

def job():
    print("I'm working...")

schedule.every().day.at("19:37").do(job)


while True:
    schedule.run_pending()
    time.sleep(1)