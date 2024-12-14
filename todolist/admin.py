from django.contrib import admin

from todolist.models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'priority', 'is_completed')
    search_fields = ('title', 'description')

    