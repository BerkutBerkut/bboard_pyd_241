from django.db.models import Count
from django.contrib.auth.models import User, Group

from django.shortcuts import redirect
from django.conf import settings

from bboard.models import Rubric


EXEMPT_URLS = [
    settings.LOGIN_URL,
    '/logout/',
    '/register/',
]
# Middleware для перенаправления неавторизованных пользователей на страницу входа.
class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    # def __call__(self, request):
    #     if not request.user.is_authenticated and request.path not in [settings.LOGIN_URL, '/admin/']:
    #         return redirect(settings.LOGIN_URL)  # Перенаправляем на страницу входа
    #     return self.get_response(request)

    def __call__(self, request):
        if not request.user.is_authenticated and not any(request.path.startswith(url) for url in EXEMPT_URLS):
            return redirect(settings.LOGIN_URL)  # Перенаправляем на страницу входа
        return self.get_response(request)


# Посредник функция
def my_middleware(next):
    # Какая-то инициализация
    def core_middleware(request):
        # Какая-то обработка клиентского запроса
        response = next(request)
        # обработка ответа
        return response
    return core_middleware


# Посредники классы
class MyMiddleware:
    def __init__(self, next):
        self.next = next
        # Какая-то инициализация

    def __call__(self, request):
        # Отбработка клиентского запроса
        response = self.next(request)
        # обработка ответа
        return response


class RubbricMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_template_response(self, request, response):
        print('MIDDLEWARE')
        response.context_data['rubrics'] = Rubric.objects.all()
        return response


# Обработчики контекста 'context_processors'
def rubrics(request):
    # return {'rubrics': Rubric.objects.all()}
    return {"rubrics": Rubric.objects.annotate(cnt=Count("bb")).filter(cnt__gt=0)}


# Обработчик контекста обо всех пользователях
# def all_users(request):
#     return {'all_users': User.objects.all()}

# Обработчик контекста о пользователях и группах текущего пользователя
def all_users_group(request):
    user_groups = Group.objects.filter(user=request.user) if request.user.is_authenticated else []
    return {'all_users': User.objects.all(), 'user_groups': user_groups}
