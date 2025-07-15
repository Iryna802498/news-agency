from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Topic, Newspaper, Redactor
from .forms import (
    TopicForm,
    NewspaperForm,
    RedactorCreationForm,
    RedactorExperienceUpdateForm,
)


@login_required
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


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    context_object_name = "topic_list"
    template_name = "agency/topic_list.html"
    paginate_by = 3


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    success_url = reverse_lazy("agency:topic-list")
    template_name = "agency/topic_form.html"
    form_class = TopicForm


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("agency:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("agency:topic-list")


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    queryset = Newspaper.objects.prefetch_related("topic", "publishers")
    context_object_name = "newspaper_list"
    template_name = "agency/newspaper_list.html"
    paginate_by = 3


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("agency:newspaper-list")
    template_name = "agency/newspaper_form.html"


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    fields = "__all__"
    success_url = reverse_lazy("agency:newspaper-list")


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    fields = ["title",]
    success_url = reverse_lazy("agency:newspaper-list")


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    paginate_by = 3


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.all().prefetch_related("newspapers__topic")


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create redactor"
        return context


class RedactorYearsExperienceUpdateView(
        LoginRequiredMixin,
        generic.UpdateView):
    model = Redactor
    form_class = RedactorExperienceUpdateForm
    success_url = reverse_lazy("agency:redactor-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update years of experience"
        return context


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Redactor
    success_url = reverse_lazy("agency:redactor-list")
