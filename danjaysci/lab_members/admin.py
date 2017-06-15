from django.contrib import admin

from .models import LabMember, LabPosition

# Register your models here.
admin.site.register(LabMember)
admin.site.register(LabPosition)

