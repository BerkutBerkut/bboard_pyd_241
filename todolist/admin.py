from django.contrib import admin
from todolist.models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', "updated_at", "completed", "created_at") # Отображаемые поля
    list_filter = ('completed', 'updated_at') # Фильтрация по полям
    search_fields = ('title', 'description') # Поиск по названию и описанию задачи
    list_editable = ('completed',) # Возможность редактировать статус выполнения
    ordering = ('-created_at',) # Сортировка по дату создания
    date_hierarchy = 'created_at' # Иерархия по дате

