
from django.contrib import admin

# Register your models here.
from .models import System_User, Groups_engineer, Company, User_type, Contract, Request
from .models import Request_status, Request_type, Request_priority, Normative_time, Specialization, Storage, Replacement


class RequestTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'info')


admin.site.register(System_User)
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



