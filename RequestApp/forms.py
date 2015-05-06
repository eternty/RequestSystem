__author__ = 'eternty'
from django import forms
from django.forms import ModelForm
from RequestApp.models import Request, Equipment, Comment


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class RequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ['company', 'creator', 'reqtype', 'priority', 'header', 'info',  'equipment' ]



class ClientRequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ['reqtype', 'priority', 'header', 'info',  'equipment']

class ShowRequestForm(ModelForm):
    class Meta:
        model = Request
        exclude = ['id', 'company', 'header', 'info', 'approvement','createtime','mark', 'solution' ]

class NewCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']