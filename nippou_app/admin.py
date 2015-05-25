from django.contrib import admin
from nippou_app.models import nippou_data

# Register your models here.
class nippou_dataAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date',)
    list_display_links = ('id', 'title',)

admin.site.register(nippou_data, nippou_dataAdmin)