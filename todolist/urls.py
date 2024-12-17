from django.urls import path, re_path

from todolist import views

from todolist.views import (
    todo_list,
    todo_detail,
    todo_create,
    todo_update,
    todo_delete,
    todo_edit,
)

app_name = 'todolist'

urlpatterns = [
    path('', todo_list, name='todo_list'),
    path('<int:todo_id>/', todo_detail, name='todo_detail'),
    path('create/', todo_create, name='todo_create'),
    path('update/<int:todo_id>/', todo_update, name='todo_update'),
    path('delete/<int:todo_id>/', todo_delete, name='todo_delete'),
]


urlpatterns = [
    re_path(r"^todolist/$", views.todo_list, name="todo_list"), # Список всех задач.
    re_path(r"^todolist/(?P<todo_id>\d+)/$", views.todo_detail, name="todo_detail"), # Детальный просмотр задачи по её ID.
    re_path(r"^todolist/create/$", views.todo_create, name="todo_create"), # Страница для создания новой задачи.
    re_path(r"^todolist/(?P<todo_id>\d+)/edit/$", views.todo_edit, name="todo_edit"), # Редактирование задачи по ID.
    re_path(r"^todolist/(?P<todo_id>\d+)/delete/$", views.todo_delete, name="todo_delete"), # Удаление задачи по ID.
]
