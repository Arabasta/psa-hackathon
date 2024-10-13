import random
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from firebase_config import db
from services import set_bomen_of_the_day

scheduler = AsyncIOScheduler()
fun_facts = [
    "fun fact1",
    "fun fact2",
    "fun fact3",
]
fun_fact_index = 0

def set_bomen_scheduler():
    global fun_fact_index
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_str = yesterday.isoformat()

    # get yesterday's submissions
    docs = db.collection("submissions").where("dateTime", ">=", yesterday_str).stream()
    submissions = [doc.to_dict() for doc in docs]

    if submissions:
        random_submission = random.choice(submissions)
        random_bomen = {
            "imageURL": random_submission["imageURL"],
            "imageCaption": random_submission["imageCaption"],
            "fun_fact": fun_facts[fun_fact_index]
        }
        # set in memory cache
        set_bomen_of_the_day(random_bomen)
        fun_fact_index = (fun_fact_index + 1) % len(fun_facts)


def schedule_bomen_job():
    # run at midnight sg time
    scheduler.add_job(set_bomen_scheduler, 'cron', hour=0, minute=0, timezone='Asia/Singapore')
    scheduler.start()
