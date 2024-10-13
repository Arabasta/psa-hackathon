import random
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from firebase_config import db
from services import set_bomen_of_the_day

scheduler = AsyncIOScheduler()
fun_facts = [
    "Generally displayed in groups, the Bo-men stride forward with passion and purpose, moving towards a common goal.",
    "The Bo-men sculptures celebrate human potential, resilience and the spirit of collaboration, which echo themes "
    "central to PSA’s core ethos.",
    "The Bo-men's form transcends race and nationality, connecting instead with the common thread that is humanity."
    "PSA Singapore has a global network encompassing 179 locations in 45 countries.",
    "We operate the world's largest container transhipment hub.",
    "About 85 per cent of the containers that arrive in Singapore are transhipped to another port of call.",
    "total of 36 ‘Bo-men’ of varying sizes now reside in the PSA Horizons building in Singapore, alongside 11 in our "
    "upcoming Tuas Port.",
    "The Bo-men can be found at key points starting from the drop off foyer to the main lobby and up through the "
    "building to the sky garden’s above.",
    "Through the art of sculpture, Daisy and her Bo-men embody this same spirit of being Alongside in their form and "
    "posture, conveying this unity of purpose with diversity, equity and inclusion, suspended in time.",
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
