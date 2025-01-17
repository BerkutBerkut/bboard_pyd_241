from django import forms
from django.forms import ModelForm
from captcha.fields import CaptchaField

from todolist.models import Todo


class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = '__all__'


class SimpleForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100, required=True)
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea,
        required=False
    )
    completed = forms.BooleanField(label="Completed", required=False)
    captcha = CaptchaField()

