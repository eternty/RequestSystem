
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
    list_display = ('id', 'header', 'company', 'creator', 'createtime', 'reqtype', 'priority', 'status')

class RequestPriorityAdmin(admin.ModelAdmin):
    list_display = ('name','info')

class NormativeTimeAdmin(admin.ModelAdmin):
    list_display = ('reqtype', 'priority', 'status', 'time_value')

class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('engineer', 'group')

class StorageAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'income_date', 'outcome_date', 'target_equipment')

class ReplacementAdmin(admin.ModelAdmin):
    list_display = ('crashed', 'replace')

class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial', 'contract', 'address')

class ExecutionTimeAdmin(admin.ModelAdmin):
    list_display = ('request', 'rstatus', 'start_exectime', 'finish_exectime')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('request', 'author', 'content', 'date_time')

admin.site.register(System_User, SystemUserAdmin)
admin.site.register(Groups_engineer, GroupsEngineerAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(User_type,UserTypeAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Request_status, RequestTypeAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(Request_type, RequestTypeAdmin)
admin.site.register(Request_priority, RequestPriorityAdmin)
admin.site.register(Normative_time, NormativeTimeAdmin)
admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(Storage, StorageAdmin)
admin.site.register(Replacement, ReplacementAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Execution_time, ExecutionTimeAdmin)
admin.site.register(Comment, CommentAdmin)




