from django.db import models

# Create your models here.


class EpisodeModels(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    publish_date = models.DateTimeField(0)
    link = models.URLField()
    image = models.URLField()
    creator_name = models.CharField(max_length=100)
    guid = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.creator_name}: {self.title}"
