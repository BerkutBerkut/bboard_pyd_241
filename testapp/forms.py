from django import forms

class UserSearchForm(forms.Form):
    user_id = forms.IntegerField(label="Введите ID пользователя:", min_value=1)

    