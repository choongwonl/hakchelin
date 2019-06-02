from django.contrib import admin

# Register your models here.
from reviews.models import CustomReview, CustomCheck

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author', 'mid', 'created', 'star', 'comment']
    raw_id_fields = ['author']
    list_filter = ['created', 'author', 'star']
    search_fields = ['comment', 'created']
    ordering = ['-created']



admin.site.register(CustomReview, ReviewAdmin)

class CheckAdmin(admin.ModelAdmin):
    list_display = ['cid', 'created', 'author']
    raw_id_fields = ['author']
    list_filter = ['created', 'author']
    ordering = ['-created']

admin.site.register(CustomCheck, CheckAdmin)