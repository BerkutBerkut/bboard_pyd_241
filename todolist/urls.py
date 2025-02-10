from django.urls import path
# from django.urls import re_path
from django.shortcuts import render, redirect, get_object_or_404

# from todolist.views import (todo_list, todo_detail, todo_create,
#                             todo_update, todo_delete)
from todolist.views import (
    todo_archived,
    todo_search,
    simple_form,
    handle_form,
    upload_img,
    upload_doc,
    success,
    img_list,
    doc_list,
    delete_img,
    delete_doc,
    secure_task,
    verify_task
)
from todolist.views import (IndexView, TodoListView, TodoDetailView, 
                            TodoCreateView, TodoDeleteView, TodoUpdateView)

app_name = 'todolist'

urlpatterns = [
    path("", IndexView.as_view(), name="todo_index"),
    # path("", todo_list, name="todo_list"),
    path("todo_list/", TodoListView.as_view(), name="todo_list"),
    # re_path(r"^$", todo_list, name="todo_list"),
    # path("todo_detail/<int:todo_id>/", todo_detail, name="todo_detail"),
    path("todo_detail/<int:pk>/", TodoDetailView.as_view(), name="todo_detail"),
    # re_path(r"^(?P<todo_id\d+>)/$", todo_detail, name="todo_detail"),
    # path("todo_create/", todo_create, name="todo_create"),
    path("todo_create/", TodoCreateView.as_view(), name="todo_create"),
    # re_path(r"^create/$", todo_create, name="todo_create"),
    path("todo_update/<int:pk>/", TodoUpdateView.as_view(), name="todo_update"),
    # re_path(r"^update/(?P<todo_id>\d+)/$", todo_update, name="todo_update"),
    # path("todo_delete/<int:todo_id>/", todo_delete, name="todo_delete"),
    path("todo_delete/<int:pk>/", TodoDeleteView.as_view(), name="todo_delete"),
    # re_path(r"^delete/(?P<todo_id>\d+)/$", todo_delete, name="todo_delete"),
    path("todo_archived/<int:todo_id>/", todo_archived, name="todo_archivede"),
    path("todo_search/<int:todo_id>/", todo_search, name="todo_search"),
    path("simple_form/", simple_form, name="simple_form"),
    path("handle_form/", handle_form, name="handle_form"),
    path("upload_img/", upload_img, name="upload_img"),
    path("upload_doc/", upload_doc, name="upload_doc"),
    path("success/", success, name="success"),
    path("img_list/", img_list, name="img_list"),
    path("doc_list/", doc_list, name="doc_list"),
    path("delete_img/<int:pk>/", delete_img, name="delete_img"),
    path("delete_doc/<int:pk>/", delete_doc, name="delete_doc"),

    path("secure_task/", secure_task, name="secure_task"),
    path("verify_task/<str:signed_task>/", verify_task, name="verify_task"),
]
