from django.db import models
from django.contrib.auth.models import AbstractUser
from news_agency import settings


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    topic = models.ManyToManyField(
        Topic,
        related_name="newspapers",
    )
    publishers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="newspapers",
    )

    class Meta:
        ordering = [
            "title",
            "-published_date",
        ]

    def __str__(self) -> str:
        return self.title


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(default=0)

    class Meta:
        ordering = [
            "username",
        ]

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"
