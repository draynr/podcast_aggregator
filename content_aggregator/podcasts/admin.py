from django.contrib import admin


from django.contrib import admin

from .models import EpisodeModels


@admin.register(EpisodeModels)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ["creator_name", "title", "publish_date"]

# Register your models here.
