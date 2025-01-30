from django.contrib.auth import get_user, authenticate, login, logout

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib import messages

from django.core.paginator import Paginator
from django.db import transaction, DatabaseError
from django.db.models import Count
from django.forms import modelformset_factory
from django.forms.models import inlineformset_factory
from django.http import (HttpResponse, HttpResponseRedirect, HttpResponseNotFound,
                         Http404, StreamingHttpResponse, FileResponse, JsonResponse)
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.template import loader
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import (require_http_methods,
                                          require_GET, require_POST, require_safe)
from django.views.generic.base import RedirectView
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView

from bboard.forms import BbForm, RubricBaseFormSet, IcecreamForm,  SearchForm
from bboard.models import Bb, Rubric, Icecream, Img

import logging

# Основной (вернуть)
# def index(request):
#     bbs = Bb.objects.order_by('-published')
#     # rubrics = Rubric.objects.all()
#     rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
#     context = {'bbs': bbs, 'rubrics': rubrics}
#
#     return render(request, 'bboard/index.html', context)


def index(request):

    bbs = Bb.objects.order_by('-published')
    # rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)

    paginator = Paginator(bbs, 2)

    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1

    page = paginator.get_page(page_num)

    # context = {'bbs': page.object_list, 'rubrics': rubrics, 'page': page}


    # Учет через счетчик
    # if "counter" in request.COOKIES:
    #     cnt = int(request.COOKIES["counter"]) + 1
    # else:
    #     cnt = 1

    # context = {"bbs": page.object_list, "page": page, 'counter':cnt}

    # response = render(request, 'bboard/index.html', context)
    # response.set_cookie('counter', cnt)
    # return response

    # Учет через сессию
    if "counter" in request.session:
        cnt = request.session["counter"] + 1
    else:
        cnt = 1

    request.session['counter'] = cnt

    context = {"bbs": page.object_list, "page": page, 'counter':cnt}

    return render(request, 'bboard/index.html', context)

    # if not request.user.is_authenticated:
    #     return redirect(
    #         "bboard:login"
    #     )  # Если пользователь не авторизован, отправляем на страницу входа

    # return render(request, 'bboard/index.html', context)


class BbIndexView(ArchiveIndexView):
    model = Bb
    date_field = 'published'
    date_list_period = 'year'
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(
                                            cnt=Count('bb')).filter(cnt__gt=0)
        return context


class BbRedirectView(RedirectView):
    url = '/'


def by_rubric(request, rubric_id):
    # bbs = Bb.objects.filter(rubric=rubric_id)
    bbs = get_list_or_404(Bb, rubric=rubric_id)
    # rubrics = Rubric.objects.all()
    # rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    current_rubric = Rubric.objects.get(pk=rubric_id)

    # bbs = current_rubric.entries.all()

    # context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    context = {"bbs": bbs, "current_rubric": current_rubric}

    return render(request, 'bboard/by_rubric.html', context)


# Основной, вернуть
class BbRubricBbsView(ListView):
    template_name = 'bboard/rubric_bbs.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['rubrics'] = Rubric.objects.annotate(
        #                                     cnt=Count('bb')).filter(cnt__gt=0)
        context['current_rubric'] = Rubric.objects.get(
                                                   pk=self.kwargs['rubric_id'])
        return context


# class BbRubricBbsView(SingleObjectMixin, ListView):
#     template_name = 'bboard/rubric_bbs.html'
#     pk_url_kwarg = 'rubric_id'
#
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object(queryset=Rubric)
#         return super().get(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['current_rubric'] = self.object
#         context['rubrics'] = Rubric.objects.all()
#         context['bbs'] = context['object_list']
#         return context
#
#     def get_queryset(self):
#         return self.object.bb_set.all()


# Основной (вернуть)
class BbCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'bboard/bb_create.html'
    model = Bb
    form_class = BbForm
    success_url = reverse_lazy('bboard:index')
    # initial = {'price': 1000.0}

    def test_func(self):
        return self.request.user.is_staff

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['rubrics'] = Rubric.objects.annotate(
    #                                         cnt=Count('bb')).filter(cnt__gt=0)
    #     return context


def add_and_save(request):
    if request.method == 'POST':
        bbf = BbForm(request.POST)

        # bbf = BbForm(request.POST, request.FILES)

        # bbf = BbForm(request.POST, request.FILES)
        # if bbf.is_valid():
        #     for file in request.FILES.getlist('img'):
        #         img = Img()
        #         img.desc = bbf.cleaned_data['desc']
        #         img.img = file
        #         img.save()


        if bbf.is_valid():
            bbf.save()
            # return HttpResponseRedirect(reverse('bboard:by_rubric',
            #             kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
            return redirect('bboard:by_rubric',
                            rubric_id=bbf.cleaned_data['rubric'].pk)
        else:
            context = {'form': bbf}
            return render(request, 'bboard/bb_create.html', context)
    else:
        # bbf = BbForm(initial={'price': 1000.0})
        bbf = BbForm()
        context = {'form': bbf}
        return render(request, 'bboard/bb_create.html', context)


# Основной, вернуть
class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = reverse_lazy('bboard:index')
    success_message = 'Объявление успешно исправлено!'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['rubrics'] = Rubric.objects.annotate(
    #                                         cnt=Count('bb')).filter(cnt__gt=0)
    #     return context


def edit(request, pk):
    bb = Bb.objects.get(pk=pk)
    if request.method == 'POST':
        bbf = BbForm(request.POST, instance=bb)
        if bbf.is_valid():
            # if bbf.has_changed():
            bbf.save()
            return HttpResponseRedirect(reverse('bboard:by_rubric',
                        kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request, 'bboard/bb_form.html', context)
    else:
        bbf = BbForm(instance=bb)
        context = {'form': bbf}
        return render(request, 'bboard/bb_form.html', context)


def bb_detail(request, bb_id):
    try:
        # bb = Bb.objects.get(pk=bb_id)
        bb = get_object_or_404(Bb, pk=bb_id)
    except Bb.DoesNotExist:
        # return HttpResponseNotFound('Такое объявление не существует')
        return Http404('Такое объявление не существует')

    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    context = {'bb': bb, 'rubrics': rubrics}

    return render(request, 'bboard/bb_detail.html', context)


class BbDetailView(DetailView):
    model = Bb

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['rubrics'] = Rubric.objects.annotate(
    #                                         cnt=Count('bb')).filter(cnt__gt=0)
    #     return context


class BbDeleteView(DeleteView):
    model = Bb
    success_url = '/{rubric_id}/'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['rubrics'] = Rubric.objects.annotate(
    #                                         cnt=Count('bb')).filter(cnt__gt=0)
    #     return context


@login_required(login_url='/login/')
@user_passes_test(lambda user: user.is_staff)
# @permission_required('bboard.add_rubric')
def rubrics(request):
    RubricFormSet = modelformset_factory(Rubric, fields=('name',),
                                         can_order=True,
                                         can_delete=True,
                                         formset=RubricBaseFormSet,
                                         # extra=3
                                         )

    if request.method == 'POST':
        formset = RubricFormSet(request.POST)
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                if form.cleaned_data:
                    rubric = form.save(commit=False)
                    if rubric in formset.deleted_objects:
                        rubric.delete()
                    else:
                        if form['ORDER'].data:
                            rubric.order = form['ORDER'].data
                        rubric.save()
            return redirect('bboard:index')
    else:
        formset = RubricFormSet()
    context = {'formset': formset}
    return render(request, 'bboard/rubrics.html', context)


def bbs(request, rubric_id):
    BbsFormSet = inlineformset_factory(Rubric, Bb,
                                       form=BbForm, extra=1)
    rubric = Rubric.objects.get(pk=rubric_id)
    if request.method == 'POST':
        formset = BbsFormSet(request.POST, instance=rubric)
        if formset.is_valid():
            formset.save()
            return redirect('bboard:index')
    else:
        formset = BbsFormSet(instance=rubric)
    context = {'formset': formset, 'current_rubric': rubric}
    return render(request, 'bboard/bbs.html', context)



@login_required
def user_info(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    print(f"Имя пользователя {user.username}")
    print(f"Является ли суперпользователем: {user.is_superuser}")
    print(f"Группы пользователя: {[group.name for group in user.groups.all()]}")
    return render(request, 'bboard/user_info.html', {'user': user})



def commit_handler():
    pass
    # Действия после подтверждения транзакции


# def add_icecream(request):
#     if request.method == "POST":
#         form = IcecreamForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('icecream_list'))
#     else:
#         form = IcecreamForm()

#     return render(request, 'bboard/add_icecream.html', {'form': form})


def icecream_list(request):
    icecreams = Icecream.objects.all()
    return render(request, 'bboard/icecream_list.html', {'icecreams': icecreams})


# # Новый контроллер с разделенной логикой
# def create_icecream(request):
#     if request.method == "POST":
#         form = IcecreamForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponse("Мороженое успешно добавлено!")
#         else:
#             return render(
#                 request,
#                 'create_icecream.html',
#                 {'form': form, 'error': 'Форма заполнена некорректно!'},
#             )
#     else:
#         form = IcecreamForm()
#     return render(request, 'bboard/create_icecream.html', {'form': form})


# Контроллер для работы с набором форм
def manage_icecreams(request):
    # Создаем набор форм
    IcecreamFormSet = modelformset_factory(
        Icecream, fields=("name", "content", "price"), extra=1, can_delete=True
    )

    if request.method == "POST":
        formset = IcecreamFormSet(request.POST)
        if formset.is_valid():
            # Сохраняем данные в базу
            formset.save()
            return redirect("success")  # Перенаправляем на страницу отзыва
        else:
            print(formset.errors)
            return render(
                request,
                'bboard/manage_icecreams.html',
                {'formset': formset, 'error': 'Форма содержит ошибки!'},
            )

    else:
        # Показываем пустой набор форм или заполняем существующими данными
        formset = IcecreamFormSet(queryset=Icecream.objects.all())

    return render(request, 'bboard/manage_icecreams.html', {'formset': formset})


# Контроллер успешной обработки
def success_view(request):
    return render(request, 'bboard/success.html')


# @transaction.non_atomic_requests # не атомарные запросы 'ATOMIC_REQUEST': False,
# @transaction.atomic  # атомарные запросы 'ATOMIC_REQUEST': True
def my_view(request):
    # if formset.is_valid():
    #     with transaction.atomic():
    #         for form in formset:
    #             if form.cleaned_data:
    #                 with transaction.atomic():
    #                     pass

    # try:
    #     with transaction.atomic():
    #         # сохранить данные в БД
    #         pass
    # except DatabaseError:
    #     # Реагируем на ошибки
    #     pass

    # bbs = Bb.objects.select_for_update().filter(price__lt=100)
    bbs = Bb.objects.select_for_update(skip_locked=True,
                                       of=('self', 'rubric')).filter(price__lt=100)
    # with transaction.atomic():
    #     for bb in bbs:
    #         bb.price = 100
    #         bb.save()

    # if form.is_valid():
    #     try:
    #         form.save()
    #         transaction.commit()
    #     except:
    #         transaction.rollback()

    # if formset.is_valid():
    #     for form in formset:
    #         if form.cleaned_data:
    #             sp = transaction.savepoint()
    #             try:
    #                 form.save()
    #                 transaction.savepoint_commit(sp)
    #             except:
    #                 transaction.savepoint_rollback(sp)
    #             transaction.commit()

    #             transaction.on_commit(commit_handler)

    return redirect('bboard:index')

# Форма не связанная с моделью
def search(request):
    if request.method == 'POST':
        sf = SearchForm (request.POST)
        if sf.is_valid():
            keyword = sf.cleaned_data['keyword']
            rubric_id = sf.cleaned_data['rubric'].pk
            # bbs = Bb.objects.filter(title__icontains=keyword, rubric=rubric_id)
            bbs = Bb.objects.filter(title__iregex=keyword, rubric=rubric_id)

            messages.add_message(request, messages.SUCCESS,
                                 'Слово найдено!', extra_tags='first second')

            # messages.success(request, "Слово найдено!")

            context = {'bbs': bbs, 'form': require_safe}
            return render(request, 'bboard/search_results.html', context)

    else:
        sf = SearchForm ()

    context = {'form': sf}
    return render(request, 'bboard/search.html', context)

# Возвращение строки на фронтенд
def return_string(request):
    return HttpResponse("Hello, this is a plain text string!")

# Возвращение строки с HTML-тегами
def return_html(request):
    html_content = "<h1>Welcome to Django!</h1><p>This is a response eith HTML tags.</p>"
    return HttpResponse(html_content)

# Формирование массива данных
def return_json(request):
    # Список данных, сгенерированный с помощью list comprehesion
    data_list = [f"Item {i}" for i in range(1, 11)] # Создаем массив
    return JsonResponse({"data": data_list})

# Получение параметров запроса
def show_request_parameters(request):
    if request.method == 'GET':
        params = request.GET.dict() # Получение параметров GET
    elif request.method == "POST":
        params = request.POST.dict()  # Получение параметров POST
    else:
        params = {}

    return JsonResponse(params)

# Перенаправление при отсутствии логина
def check_login(request):
    if not request.user.is_authenticated: # Проверка авторизации Usera
        return redirect('/login/') # Перенаправление на страницу логина
    return JsonResponse({"message": "Вы вошли в систему."})

# Контроллер для логирования
logger = logging.getLogger('django.request')

def log_request_data(request):
    if request.method == 'GET':
        params = request.GET.dict()
    elif request.method == 'POST':
        params = request.POST.dict()
    else:
        params = {}

    # логируем данные запроса
    logger.info(f"Request Method: {request.method}, Parameters: {params}")

    return JsonResponse({"message": "Request logged successfully"})


# удаление картинок
def delete_img(request, pk):
    img = Img.objects.get(pk=pk)
    img.img.delete(save=False)
    img.delete()
    return redirect('bboard:index')

# контроллеры метод для логирования
# def my_login(request):
#     user_name = request.POST['username']
#     pass_word = request.POST['password']
#     user = authenticate(request, username=user_name, password=pass_word)

#     if user is None:
#         login(request, user)
#         return render(request, 'bboard/login.html',
#                       {'user': user})

#     return redirect('bboard:index')


# контроллер метод для логирования
def my_login(request):
    if request.method == "POST":
        user_name = request.POST.get(
            "username"
        )  # Используем get(), чтобы избежать ошибок
        pass_word = request.POST.get(
            "password"
        )  # Используем get(), чтобы избежать ошибок

        user = authenticate(request, username=user_name, password=pass_word)

        if user is not None:
            login(request, user)
            return redirect("bboard:index")  # Перенаправляем на главную после входа
        else:
            return render(
                request,
                "bboard/login.html",
                {"error": "Неверное имя пользователя или пароль"},
            )
    else:
        return render(request, "bboard/login.html")  # Для GET-запроса


# контроллеры метод для разлогирования
def my_logout(request):
    logout(request)
    return redirect("bboard:login")  # Перенаправляем на страницу входа

# Контроллер для контекстного обработчика
def all_users_group_view(request):
    return render(request, "bboard/context_user_groups.html")
