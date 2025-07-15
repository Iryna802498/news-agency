from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Topic, Newspaper, Redactor


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = "__all__"


class NewspaperForm(forms.ModelForm):
    class Meta:
        model = Newspaper
        fields = "__all__"
        widgets = {
            "topic": forms.CheckboxSelectMultiple(),
            "publishers": forms.CheckboxSelectMultiple(),
        }


class RedactorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "years_of_experience",
            "first_name",
            "last_name",
        )
    
    def clean_years_of_experience(self):
        years = self.cleaned_data["years_of_experience"]
        if years < 0:
            raise ValidationError("Years of experience cannot be negative.")
        return years
    

class RedactorExperienceUpdateForm(forms.ModelForm):
    class Meta:
        model = Redactor
        fields = ["years_of_experience"]

    def clean_years_of_experience(self):
        years = self.cleaned_data["years_of_experience"]
        if years < 0:
            raise ValidationError("Years of experience cannot be negative.")
        return years
