from django.contrib import admin
from nippou_app.models import nippou_data
from nippou_app.models import Task
from nippou_app.models import User
import nippou_app

# Register your models here.
class nippou_dataAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date','user', 'text',)
    list_display_links = ('id', 'title','date','user', 'text')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('nippou', 'task_name', 'time_yotei', 'time_jitsu','task_y', 'task_w', 'task_t',)
    list_display_links = ('nippou', 'task_name', 'time_yotei', 'time_jitsu','task_y', 'task_w', 'task_t',)

admin.site.register(nippou_data, nippou_dataAdmin)
admin.site.register(nippou_app.models.User)
admin.site.register(Task, TaskAdmin)