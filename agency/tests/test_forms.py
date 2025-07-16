from django.contrib.auth import get_user_model
from django.test import TestCase
from agency.forms import (TopicForm,
                          NewspaperForm,
                          RedactorCreationForm,
                          RedactorExperienceUpdateForm,
                          RedactorSearchForm,
                          TopicSearchForm,
                          NewspaperSearchForm)


class FormValidationTest(TestCase):
    def test_topic_form_valid(self):
        form = TopicForm(data={"name":"Culture"})
        self.assertTrue(form.is_valid())
    
    def test_newspaper_form_valid_empty(self):
        form = NewspaperForm(
            data={
                "title": "Title Form",
                "content": "Some content.",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("topic", form.errors)
        self.assertIn("publishers", form.errors)
    
    def test_redactor_form_valid(self):
        form = RedactorCreationForm(
            data={
                "username": "test.username",
                "password1": "test1234strong",
                "password2": "test1234strong",
                "first_name": "test_first",
                "last_name": "test_last",
                "years_of_experience": 3,
            }
        )
        self.assertTrue(form.is_valid())
    
    def test_redactor_creation_form_invalid_experience(self):
        form_data = {
            "username": "test.username",
            "password1": "test1234strong",
            "password2": "test1234strong",
            "first_name": "test_first",
            "last_name": "test_last",
            "years_of_experience": -2,
        }
        form = RedactorCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)
        self.assertEqual(
            form.errors["years_of_experience"],
            ["Years of experience cannot be negative."]
        )
    
    def test_redactor_experience_update_form_valid(self):
        redactor = get_user_model().objects.create_user(
            username="test.user",
            password="test1234",
            years_of_experience=2,
        )
        form = RedactorExperienceUpdateForm(
            data={"years_of_experience": 8},
            instance=redactor
        )
        self.assertTrue(form.is_valid())

    def test_redactor_experience_update_form_invalid(self):
        redactor = get_user_model().objects.create_user(
            username="test.user",
            password="test1234",
            years_of_experience=4,
        )
        form = RedactorExperienceUpdateForm(
            data={"years_of_experience": -1},
            instance=redactor
        )
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)
    
    def test_search_form(self):
        redactor_form = RedactorSearchForm(
            data={
                "username": "searchusername"
            }
        )
        topic_form = TopicSearchForm(
            data={
                "name": "searchname"
            }
        )
        newspaper_form = NewspaperSearchForm(
            data={
                "title": "searchtitle"
            }
        )
        self.assertTrue(redactor_form.is_valid())
        self.assertTrue(topic_form.is_valid())
        self.assertTrue(newspaper_form.is_valid())

    def test_search_form_too_long(self):
        too_long_data = "x" * 300
        redactor_form = RedactorSearchForm(
            data={
                "username": too_long_data
            }
        )
        topic_form = TopicSearchForm(
            data={
                "name": too_long_data
            }
        )
        newspaper_form = NewspaperSearchForm(
            data={
                "title": too_long_data
            }
        )
        self.assertFalse(redactor_form.is_valid())
        self.assertIn("username", redactor_form.errors)
        self.assertFalse(topic_form.is_valid())
        self.assertIn("name", topic_form.errors)
        self.assertFalse(newspaper_form.is_valid())
        self.assertIn("title", newspaper_form.errors)
