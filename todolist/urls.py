from django.urls import path
# from django.urls import re_path

from todolist.views import (todo_list, todo_detail, todo_create, 
                            todo_update, todo_delete, 
                            todo_archived, todo_search)

app_name = 'todolist'

urlpatterns = [
    path('', todo_list, name='todo_list'),
    # re_path(r"^$", todo_list, name="todo_list"),
    path('todo_detail/<int:todo_id>/', todo_detail, name='todo_detail'),
    # re_path(r"^(?P<todo_id\d+>)/$", todo_detail, name="todo_detail"),
    path('todo_create/', todo_create, name='todo_create'),
    # re_path(r"^create/$", todo_create, name="todo_create"),
    path('todo_update/<int:todo_id>/', todo_update, name='todo_update'),
    # re_path(r"^update/(?P<todo_id>\d+)/$", todo_update, name="todo_update"),
    path('todo_delete/<int:todo_id>/', todo_delete, name='todo_delete'),
    # re_path(r"^delete/(?P<todo_id>\d+)/$", todo_delete, name="todo_delete"),
    path('todo_archived/<int:todo_id>/', todo_archived, name='todo_archivede'),
    path('todo_search/<int:todo_id>/', todo_search, name='todo_search'),
]
