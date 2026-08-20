from celery_config import celery

@celery.task
def daily_reminder():

    print("Daily Reminder Task Executed")

    return "Reminder Sent"