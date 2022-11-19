from django.core.management.base import BaseCommand
import feedparser
from dateutil import parser

from podcasts.models import EpisodeModels


class Command(BaseCommand):
    def handle(self, *args, **options):
        feed = feedparser.parse("https://realpython.com/podcasts/rpp/feed")
        podcast_title = feed.channel.title
        podcast_thumbnail = feed.channel.image["href"]
        for item in feed.entries:
            if not EpisodeModels.objects.filter(guid=item.guid).exists():
                episode = EpisodeModels(
                    title=item.title, description=item.description, publish_date=parser.parse(
                        item.published),
                    link=item.link, image=podcast_thumbnail, creator_name=podcast_title, guid=item.guid)
                episode.save()
