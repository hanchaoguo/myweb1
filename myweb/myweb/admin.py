from django.contrib import admin

# Register your models here.

from myweb.models import Task
from myweb.models import Cmdb

admin.site.register(Task)
admin.site.register(Cmdb)