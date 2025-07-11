from django.shortcuts import render
from .models import Topic, Newspaper, Redactor


def index(request):
    """View fuction for the home page of the site."""
    context = {
        "num_topics": Topic.objects.count(),
        "num_newspapers": Newspaper.objects.count(),
        "num_redactors": Redactor.objects.count(),
    }
    return render(
        request,
        "agency/index.html",
        context=context
    )

