from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json

from todolist.models import Todo

# Получение всех задач
def todo_list(request):
    tasks = Todo.objects.all().values("id", "title", "description", "completed", "created_at", "updated_at")
    return JsonResponse(list(tasks), safe=False)

# Получение одной задачи
def todo_detail(request, todo_id):
    task = get_object_or_404(Todo, id=todo_id)
    return JsonResponse({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
    })
    # return render(request, 'todo_detail.html')

# Создание задачи
@csrf_exempt
def todo_create(request):
    if request.method == "POST":
        data = json.loads(request.body)
        task = Todo.objects.create(
            title=data.get("title"),
            description=data.get("description", ""),
            completed=data.get("completed", False),
        )
        return JsonResponse({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
        }, status=201)
    return HttpResponse(status=405) 
    # return render(request, 'todo_create.html')

# Удаление задачи
@csrf_exempt
def todo_delete(request, todo_id):
    if request.method == "DELETE":
        task = get_object_or_404(Todo, id=todo_id)
        task.delete()
        return JsonResponse({"message": "Task deleted successfuly!"}, status=200)
    return HttpResponse(status=405)
    


def todo_update(request, todo_id):
    pass


def todo_archived(request, todo_id):
    pass


def todo_search(request, todo_id):
    pass
