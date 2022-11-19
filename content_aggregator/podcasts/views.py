
# Create your views here.
from django.views.generic import ListView

from .models import EpisodeModels


class HomePageView(ListView):
    template_name = "homepage.html"
    model = EpisodeModels

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["episodes"] = EpisodeModels.objects.filter().order_by(
            "-publish_date")[:25]
        return context
