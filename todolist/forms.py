from django import forms
from django.forms import ModelForm
from captcha.fields import CaptchaField
from django.core import validators
from django.core.exceptions import ValidationError

from todolist.models import Todo, Img, Doc


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
    # captcha = CaptchaField()

class ImgForm(ModelForm):
    img = forms.ImageField(label='Изображение',
                           validators=[validators.FileExtensionValidator(
                               allowed_extensions=('gif', 'jpg', 'png'))], 
                           error_messages={'Invalid_extension': 'Этот формат не поддерживается!'}
                           )
    
    desc = forms.CharField(label='Описание',
                           widget=forms.widgets.Textarea())
    
    class Meta:
        model = Img
        fields = '__all__'


class DocForm(ModelForm):
    file = forms.FileField(
        label="Документ",
        validators=[
            validators.FileExtensionValidator(
                allowed_extensions=("pdf", "xlsx", "docx")
            )
        ],
        error_messages={"Invalid_extension": "Этот формат не поддерживается!"},
    )

    desc = forms.CharField(label='Описание',
                           widget=forms.widgets.Textarea())
    
    class Meta:
        model = Doc
        fields = '__all__'