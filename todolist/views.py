from django.db.models import Count
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseNotFound,
    Http404,
    StreamingHttpResponse,
    FileResponse,
    JsonResponse,
)
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.template import loader
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import (
    require_http_methods,
    require_GET,
    require_POST,
    require_safe,
)
from django.views.generic.edit import CreateView

from todolist.forms import TodoForm
from todolist.models import Todo


def todo_list(request):
    tdf = TodoForm()
    context = {'form': tdf}
    return render(request, 'todo/todo_list.html')


def todo_detail(request, todo_id):
    tdf = TodoForm()
    context = {"form": tdf}
    return render(request, "todo/todo_detail.html")


def todo_create(request):
    tdf = TodoForm()
    context = {"form": tdf}
    return render(request, "todo/todo_create.html")


def todo_update(request, todo_id):
    tdf = TodoForm()
    context = {"form": tdf}
    return render(request, "todo/todo_update.html")


def todo_delete(request, todo_id):
    tdf = TodoForm()
    context = {"form": tdf}
    return render(request, "todo/todo_delete.html")
