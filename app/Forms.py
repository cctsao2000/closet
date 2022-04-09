from django import forms


class StyleForm(forms.Form):
    question1 = forms.IntegerField(widget=forms.RadioSelect)
    question2 = forms.IntegerField(widget=forms.RadioSelect)
    question3 = forms.IntegerField(widget=forms.RadioSelect)
    question4 = forms.IntegerField(widget=forms.RadioSelect)
    question5 = forms.IntegerField(widget=forms.RadioSelect)

    def saveResult(self):
        # 跑風格測驗的 Model
        pass
