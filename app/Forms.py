
import arrow

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, DNNModelTester, SecondHandPost

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


class SecondHandPostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = SecondHandPost
        fields = ('title', 'content', 'amount')
        
    def save(self, commit=False):
        obj = super().save(commit=False)
        obj.time = arrow.now().datetime
        obj.user = self.user
        obj.save()
        return obj
        


