
import logging

from django.conf import settings
from django.core.management.base import BaseCommand


import feedparser
from dateutil import parser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, DjangoJobExecution

from podcasts.models import EpisodeModels
logger = logging.getLogger(__name__)


def save_episode(feed):
    podcast_title = feed.channel.title
    podcast_thumbnail = feed.channel.image["href"]
    for item in feed.entries:
        if not EpisodeModels.objects.filter(guid=item.guid).exists():
            episode = EpisodeModels(
                title=item.title, description=item.description, publish_date=parser.parse(
                    item.published),
                link=item.link, image=podcast_thumbnail, creator_name=podcast_title, guid=item.guid)
            episode.save()


def fetch_podcast(url):
    _feed = feedparser.parse(url)
    save_episode(_feed)


def delete_old_job_executions(max_age=604_800):
    """Deletes all apscheduler job execution logs older than `max_age`."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def addJob(scheduler,  url, name, id):
    scheduler.add_job(
        fetch_podcast,
        args=[url],
        trigger="interval",
        minutes=2,
        id=id,
        max_instances=1,
        replace_existing=True,

    )

    logger.info("Added job: ", name)


class Command(BaseCommand):
    def handle(self, *args, **options):
        help = "Runs apscheduler"
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        addJob(scheduler, "https://talkpython.fm/episodes/rss",
               "Talk Python Podcast", "Talk Python Podcast")
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="Delete Old Job Executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: Delete Old Job Executions.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
