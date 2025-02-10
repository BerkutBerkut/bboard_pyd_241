from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import (ListView, DetailView, CreateView, 
                                  DeleteView, TemplateView, UpdateView)
from todolist.forms import SimpleForm, ImgForm, DocForm

from django.core.paginator import Paginator
from django.core.signing import Signer, BadSignature

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse_lazy

import json

from todolist.models import Todo, Img, Doc

class IndexView(TemplateView):
    template_name = 'todolist/todo_index.html'

# # Получение всех задач
# def todo_list(request):
#     tasks = Todo.objects.all().values("id", "title", "description", "completed", "created_at", "updated_at")
#     return JsonResponse(list(tasks), safe=False)


# Получение всех задач
class TodoListView(ListView):
    model = Todo
    template_name = 'todolist/todo_list.html'
    context_object_name = "tasks"
    
    def get(self, request, *args, **kwargs):
        tasks = self.model.objects.all()
        paginator = Paginator(tasks, 1)
        page_num = request.GET.get('page', 1)
        page = paginator.get_page(page_num)

        return render(request, self.template_name, {'page': page})


    # def render_to_response(self, context, **response_kwargs):
    #     tasks = list(
    #         context["tasks"].values(
    #             "id", "title", "description", "completed", "created_at", "updated_at"
    #         )
    #     )
    #     return JsonResponse(tasks, safe=False, **response_kwargs)


# # Получение одной задачи
# def todo_detail(request, todo_id):
#     task = get_object_or_404(Todo, id=todo_id)
#     return JsonResponse({
#         "id": task.id,
#         "title": task.title,
#         "description": task.description,
#         "completed": task.completed,
#         "created_at": task.created_at,
#         "updated_at": task.updated_at,
#     })
#     # return render(request, 'todo_detail.html')


# Получение одной задачи
class TodoDetailView(DetailView):
    model = Todo
    template_name = "todolist/todo_detail.html"
    context_object_name = "task"

    # def render_to_response(self, context, **response_kwargs):
    #     task = context["object"]
    #     return JsonResponse(
    #         {
    #             "id": task.id,
    #             "title": task.title,
    #             "description": task.description,
    #             "completed": task.completed,
    #             "created_at": task.created_at,
    #             "updated_at": task.updated_at,
    #         },
    #         **response_kwargs
    #     )


# # Создание задачи
# @csrf_exempt
# def todo_create(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         task = Todo.objects.create(
#             title=data.get("title"),
#             description=data.get("description", ""),
#             completed=data.get("completed", False),
#         )
#         return JsonResponse({
#             "id": task.id,
#             "title": task.title,
#             "description": task.description,
#             "completed": task.completed,
#             "created_at": task.created_at,
#             "updated_at": task.updated_at,
#         }, status=201)
#     return HttpResponse(status=405)
#     # return render(request, 'todo_create.html')


# Создание задачи
# @method_decorator(csrf_exempt, name="dispatch")
class TodoCreateView(SuccessMessageMixin, CreateView):
    model = Todo
    fields = ["title", "description", "completed"]
    template_name = "todolist/todo_create.html"
    success_url = reverse_lazy("todolist:todo_list")
    success_message = "Очередная задача  созданна!" # Всплывающее сообщение
    

    # def post(self, request, *args, **kwargs):
    #     data = json.loads(request.body)
    #     task = Todo.objects.create(
    #         title=data.get("title"),
    #         description=data.get("description", ""),
    #         completed=data.get("completed", False),
    #     )
    #     return JsonResponse(
    #         {
    #             "id": task.id,
    #             "title": task.title,
    #             "description": task.description,
    #             "completed": task.completed,
    #             "created_at": task.created_at,
    #             "updated_at": task.updated_at,
    #         },
    #         status=201,
    #     )


# # Удаление задачи
# @csrf_exempt
# def todo_delete(request, todo_id):
#     if request.method == "DELETE":
#         task = get_object_or_404(Todo, id=todo_id)
#         task.delete()
#         return JsonResponse({"message": "Task deleted successfuly!"}, status=200)
#     return HttpResponse(status=405)


# Удаление задачи
# @method_decorator(csrf_exempt, name="dispatch")
class TodoDeleteView(DeleteView):
    model = Todo
    template_name = "todolist/todo_delete.html"
    success_url = reverse_lazy("todolist:todo_list")
    context_object_name = 'task' 
    


    # def delete(self, request, *args, **kwargs):
    #     task = get_object_or_404(Todo, id=kwargs["pk"])
    #     task.delete()
    #     return JsonResponse({"message": "Task deleted successfully!"}, status=200)


class TodoUpdateView(UpdateView):
    model = Todo
    fields = ["title", "description", "completed"]
    template_name = "todolist/todo_update.html"
    success_url = reverse_lazy("todolist:todo_list")


def todo_archived(request, todo_id):
    pass

def todo_search(request, todo_id):
    pass


def simple_form(request):
    form = SimpleForm()
    return render(request, "todolist/simple_form.html", {"form": form})

def handle_form(request):
    if request.method == "POST":
        form = SimpleForm(request.POST)
        if form.is_valid():
            # Сохранение данных в модели Todo
            Todo.objects.create(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                completed=form.cleaned_data["completed"]
            )
            return HttpResponse("Форма обработана и задача сохранена успешно")
    else:
        form = SimpleForm()
    return render(request, "todolist/simple_form.html", {"form": form})


def success(request):
    return render(request, "todolist/success.html")


# Загрузка изображений
def upload_img(request):
    if request.method == "POST":
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            CRITICAL = 50
            # messages.success(request, "Изображение успешно добавленно!")
            messages.add_message(request, CRITICAL, "Зря ты это сделал!")
            return redirect("todolist:success")
        else:
            messages.error(request, "Ошибка при добавлений изображения") 
    else:
        form = ImgForm()
    return render(request, "todolist/upload_img.html", {"img_form": form})


# Загрузка документов
def upload_doc(request):
    if request.method == "POST":
        form = DocForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Документ успешно добавлен!")
            return redirect("todolist:success")
        else:
            messages.error(request, "Ошибка при добавлений документа")
    else:
        form = DocForm()
    return render(request, "todolist/upload_doc.html", {"doc_form": form})


# Вывод изображений
def img_list(request):
    img_objects = Img.objects.all()
    paginator = Paginator(img_objects, 1) # 1 изображение на странице
    
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1

    page = paginator.get_page(page_num)
    return render(request, "todolist/img_list.html", {"page": page})


# Вывод документов
def doc_list(request):
    doc_objects = Doc.objects.all()
    paginator = Paginator(doc_objects, 1)  # 1 документ на страницу
    page_number = request.GET.get("page")
    
    if "page" in request.GET:
        page_num = request.GET["page"]
    else:
        page_num = 1

    page = paginator.get_page(page_num)
    return render(request, "todolist/doc_list.html", {"page": page})


# удаление картинок
def delete_img(request, pk):
    img = Img.objects.get(pk=pk)
    img.img.delete(save=False)
    img.delete()
    return redirect("todolist:img_list")


# удаление файлов
def delete_doc(request, pk):
    file = Doc.objects.get(pk=pk)
    file.file.delete(save=False)
    file.delete()
    return redirect("todolist:doc_list")

signer = Signer()
# подписывание данных
def secure_task(request):
    signed_task = None

    if request.method == 'POST':
        task_id = request.POST.get("task_id") # Получение ID задачи из формы
        if task_id:
            signed_task = signer.sign(task_id) # Подписываем задачу

    return render(request, 'todolist/secure_task.html', {"signed_task": signed_task})


# проверка подписи
def verify_task(request, signed_task):
    try:
        task_id = signer.unsign(signed_task)
        message = f"Подпись верна! ID задачи: {task_id}"
    except BadSignature:
        message = f"Ошибка! Подпись недействительна или была изменена."

    return render(request, "todolist/verify_task.html", {"message": message})
