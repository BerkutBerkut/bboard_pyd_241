from django.shortcuts import render
from django.http import HttpResponse

def todo_list(request):
    return HttpResponse("Список всех задач.")

def todo_detail(request, todo_id):
    return HttpResponse(f"Детальная информация о задаче {todo_id}.")


def todo_create(request):
    return HttpResponse("Создание новой задачи.")


def todo_delete(request, todo_id):
    return HttpResponse(f"Удаление задачи {todo_id}.")


def todo_edit(request, todo_id):
    return HttpResponse(f"Редактирование задачи {todo_id}.")


def todo_update(request, todo_id):
    pass
