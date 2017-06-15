from django.contrib import admin
from .models import Institution, Department, Program, Group, Funding

# Register your models here.
admin.site.register(Institution)
admin.site.register(Department)
admin.site.register(Program)
admin.site.register(Group)
admin.site.register(Funding)
