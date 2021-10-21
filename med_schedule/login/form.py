from django import forms

class RegisterForm(forms.Form):
    path = forms.CharField(required=False)
    name = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    age = forms.IntegerField()
    gender = forms.CharField(max_length=1)
    cnumber = forms.IntegerField()

class LoginForm(forms.Form):
    path = forms.CharField(required=False)
    name = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)