from django.contrib import admin

# Register your models here.
from menus.models import CustomMenu

class MenuAdmin(admin.ModelAdmin):
    list_display = ['mid', 'date', 'title', 'location', 'review_count', 'star_count', 'avg']
    # raw_id_fields = ['mid']
    list_filter = ['date', 'location']
    search_fields = ['title', 'location']
    ordering = ['-date']

admin.site.register(CustomMenu, MenuAdmin)