from django.contrib import admin
from nippou_app.models import nippou_data
from nippou_app.models import Task
from nippou_app.models import User

# Register your models here.
class nippou_dataAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date','user', 'text', 'task')
    list_display_links = ('id', 'title','date','user', 'text', 'task')

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_pass', 'user_dev',)
    list_display_links = ('user_name', 'user_pass', 'user_dev',)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'time_yotei', 'time_jitsu','task_y', 'task_w', 'task_t',)
    list_display_links = ('task_name', 'time_yotei', 'time_jitsu','task_y', 'task_w', 'task_t',)

admin.site.register(nippou_data, nippou_dataAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Task, TaskAdmin)