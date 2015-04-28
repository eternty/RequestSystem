
from django.contrib import admin

# Register your models here.
from django import forms
from .models import *

class UserForm(forms.ModelForm):

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        if not user.password.startswith('pbkdf2_sha256$15000$'):
            user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

class SystemUserAdmin(admin.ModelAdmin):
    form = UserForm
    add_form = UserForm

class RequestTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'info')

class GroupsEngineerAdmin(admin.ModelAdmin):
    list_display = ('name', 'head', 'info')

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'manager', 'focus')

class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'info')

class ContractAdmin(admin.ModelAdmin):
    list_display = ('number', 'company', 'begin_date', 'finish_date')

class RequestStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'info')

class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'header', 'company', 'creator', 'createtime')





admin.site.register(System_User, SystemUserAdmin)
admin.site.register(Groups_engineer)
admin.site.register(Company)
admin.site.register(User_type)
admin.site.register(Contract)
admin.site.register(Request_status)
admin.site.register(Request)
admin.site.register(Request_type, RequestTypeAdmin)
admin.site.register(Request_priority)
admin.site.register(Normative_time)
admin.site.register(Specialization)
admin.site.register(Storage)
admin.site.register(Replacement)
admin.site.register(Equipment)




