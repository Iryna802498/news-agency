from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from agency.models import Topic, Newspaper, Redactor


class ModelTest(TestCase):
    def test_topic_str(self):
        topic = Topic.objects.create(name="Test_topic")
        self.assertEqual(str(topic), topic.name)

    def test_redactor_str(self):
        redactor = get_user_model().objects.create(
            username="test.username",
            password="test1234",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(redactor),
            f"{redactor.username} ({redactor.first_name} {redactor.last_name})"
        )

    def test_redactor_get_ablosute_url(self):
        redactor = get_user_model().objects.create(
            username="test.user",
            password="test1234",
        )
        expected_url = reverse(
            "agency:redactor-detail",
            kwargs={"pk": redactor.pk}
        )
        self.assertEqual(redactor.get_absolute_url(), expected_url)

    def test_newspaper_str(self):
        topic = Topic.objects.create(name="Test_topic")
        publishers = get_user_model().objects.create(
            username="test.user",
            password="test1234",
            first_name="test_first",
            last_name="test_last",
        )
        newspaper = Newspaper.objects.create(
            title="Test Title",
            content="Test content for newspaper.",
        )
        newspaper.topic.add(topic)
        newspaper.publishers.add(publishers)
        self.assertEqual(str(newspaper), newspaper.title)

    def test_create_redactor_with_experience(self):
        username = "test.user"
        password = "test1234"
        experience = 3
        redactor = get_user_model().objects.create_user(
            username=username,
            password=password,
            years_of_experience=experience,
        )
        self.assertEqual(redactor.username, username)
        self.assertTrue(redactor.check_password(password))
        self.assertEqual(redactor.years_of_experience, experience)
