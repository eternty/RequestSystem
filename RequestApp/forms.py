__author__ = 'eternty'
from django import forms
from django.forms import ModelForm
from RequestApp.models import Request, Equipment, Comment


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
        exclude = ['id', 'company', 'header', 'info', 'createtime','mark' ,'approvement', 'solution']


class ShowSolRequestForm(ModelForm):
    class Meta:
        model = Request
        exclude = ['id', 'company', 'header', 'info','createtime','mark' ]


class ShowClientRequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ['approvement']


class ShowEngRequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ['status', 'equipment', 'group',  'engineer']

class ShowEngSolRequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ['status', 'equipment',  'group',  'engineer', 'solution']

class NewCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
