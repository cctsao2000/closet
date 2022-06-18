
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, DNNModelTester

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'nickname', 'phone', 'password1', 'password2')


class StyleForm(forms.Form):
    question1 = forms.IntegerField(widget=forms.RadioSelect)
    question2 = forms.IntegerField(widget=forms.RadioSelect)
    question3 = forms.IntegerField(widget=forms.RadioSelect)
    question4 = forms.IntegerField(widget=forms.RadioSelect)
    question5 = forms.IntegerField(widget=forms.RadioSelect)

    def save_result(self):
        # 跑風格測驗的 Model
        pass


class DNNForm(forms.ModelForm):

    class Meta:
        model = DNNModelTester
        fields = ['name', 'image']
