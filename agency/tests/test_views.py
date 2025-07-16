from django.test import Client
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from agency.models import Topic, Newspaper, Redactor


TOPIC_FORMAT_URL = reverse("agency:topic-list")
NEWSPAPER_FORMAT_URL = reverse("agency:newspaper-list")
REDACTOR_FORMAT_URL = reverse("agency:redactor-list")


class PublicViewsTest(TestCase):
    def test_login_required_for_topic_and_redactor(self):
        urls = [
            TOPIC_FORMAT_URL,
            REDACTOR_FORMAT_URL,
            NEWSPAPER_FORMAT_URL,
        ]
        for url in urls:
            res = self.client.get(url)
            self.assertNotEqual(res.status_code, 200)


class PrivateTopicTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_topic(self):
        Topic.objects.create(name="Topic 1")
        Topic.objects.create(name="Topic 2")
        response = self.client.get(TOPIC_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        topics = Topic.objects.all()
        self.assertEqual(
            list(response.context["topic_list"]),
            list(topics)
        )
        self.assertTemplateUsed(response, "agency/topic_list.html")

    def test_search_topic_filters_queryset(self):
        Topic.objects.create(name="Politics")
        Topic.objects.create(name="Sports")
        response = self.client.get(TOPIC_FORMAT_URL, {"name": "Pol"})
        self.assertContains(response, "Politics")
        self.assertNotContains(response, "Sports")


class PrivateRedactorTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_create_redactor(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test First",
            "last_name": "Test Last",
            "years_of_experience": 3,
        }
        res = self.client.post(reverse("agency:redactor-create"), data=form_data)
        new_redactor = get_user_model().objects.get(username=form_data["username"])
        self.assertRedirects(
            res,
            reverse(
                "agency:redactor-detail",
                kwargs={"pk": new_redactor.pk}
            )
        )
        self.assertTrue(
            get_user_model().objects.filter(username=form_data["username"]).exists()
        )

    def test_search_redactor_filters_queryset(self):
        Redactor.objects.create_user(
            username="admin.user",
            password="Ge12349",
            years_of_experience=3
        )
        Redactor.objects.create_user(
            username="user.user",
            password="test369",
            years_of_experience=4
        )

        response = self.client.get(REDACTOR_FORMAT_URL, {"username": "adm"})
        self.assertContains(response, "admin.user")
        self.assertNotContains(response, "user.user")
        self.assertTemplateUsed(response, "agency/redactor_list.html")


class PrivateNewspaperTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_search_newspaper_filters_queryset(self):
        topic1 = Topic.objects.create(name="Test Topic")
        topic2 = Topic.objects.create(name="Test Topic 2")
        newspaper = Newspaper.objects.create(
            title="Test Title",
            content="Some content."
        )
        newspaper.topic.set([topic1, topic2])

        response = self.client.get(NEWSPAPER_FORMAT_URL, {"title": "Test Title"})
        self.assertContains(response, "Test Title")
        self.assertTemplateUsed(response, "agency/newspaper_list.html")
