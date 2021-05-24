from django import forms
from django.contrib.auth.forms import UserCreationForm
from contester.models import Account


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Account
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 1 megabytes'
    )


class SuggestingTaskForm(forms.Form):
    CHOICES = (('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard'),)
    title = forms.CharField(max_length=100)
    difficulty = forms.ChoiceField(choices=CHOICES)
    source = forms.CharField(max_length=100)
    isOriginal = forms.CheckboxInput()
    description = forms.TextInput()
    solution = forms.TextInput()


class CreateTaskForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.TextInput()
    input_description = forms.TextInput()
    output_description = forms.TextInput()
    CHOICES = (('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard'),)
    complexity = forms.ChoiceField(choices=CHOICES)
    topic = forms.CharField(max_length=100)
    points = forms.NumberInput()
