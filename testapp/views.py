from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_list_or_404, redirect
from django.core.mail import (EmailMessage, get_connection, 
                                EmailMultiAlternatives, 
                                send_mail, send_mass_mail, mail_managers)

from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import FormView
from testapp.forms import UserSearchForm
from django.utils.timezone import now
from django.template.loader import render_to_string

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from testapp.models import SMS, Profile
from testapp.serializers import UserSerializer


class SMSListView(ListView):
    model = SMS
    template_name = 'testapp/sms_list.html'
    context_object_name = 'sms_list'
    ordering = ['-timestamp']

def test_cookie(request):
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            print('КУКИ НЕ РАБОТАЮТ')
    request.session.set_test_cookie()
    print('TEST_COOKIE', request.session.test_cookie_worked())
    return render(request, 'testapp/test_cookie.html')


def test_email(request):
    ##### Низкоуровневые #####
    # em = EmailMessage(subject='Тест', body='Тест',
    #                   to=['yser@supersite.kz'])
    # em.send()

    # em = EmailMessage(
    #     subject="Ваш новый пароль.",
    #     body="Ваш новый пароль находится во вложений.",
    #     attachments=[('password.txt', '123456789', 'text/plain')],
    #     to=["user@supersite.kz"],
    # )
    # em.send()

    # em = EmailMessage(
    #     subject="Запрошенный Вами файл",
    #     body="Получите запрошенный Вами файл.",
    #     to=["user@supersite.kz"],
    # )
    # em.attach_file(r'C:\work\file.txt')
    # em.send()

    ### на основе шаблонов ###
    # context = {'user': 'Вася Пупкин'}
    # s = render_to_string('email/letter.txt', context)
    # em = EmailMessage(subject='Оповещение', body=s,
    #                   to=['vpupkin@othersite.kz'])
    # em.send()

    ### соединения, массовая рассылка ###
    # con = get_connection()
    # con.open()
    # email1 = EmailMessage(
    #     subject="Запрошенный Вами файл",
    #     body="Получите запрошенный Вами файл.",
    #     to=["user@supersite.kz"],
    #     connection=con)
    # email2 = EmailMessage(
    #     subject="Запрошенный Вами файл",
    #     body="Получите запрошенный Вами файл.",
    #     to=["user@supersite.kz"],
    #     connection=con)
    # email3 = EmailMessage(
    #     subject="Запрошенный Вами файл",
    #     body="Получите запрошенный Вами файл.",
    #     to=["user@supersite.kz"],
    #     connection=con)
    # con.send_messages([email1, email2, email3])
    # con.close()

    ### составное письмо ###
    # em = EmailMultiAlternatives(subject='Тест', body='Тест',
    #                             to=['user@supersite.kz'])
    # em.attach_alternative('<h1>Тест</h1>', 'text/html')
    # em.send()

    ##### Высокоуровневые #####
    # send_mail('Test email', 'Test!!!', 'webmaster@supersite.kz',
    #           ['user@othersite.kz'], html_message='<h1>Test!!!</h1>')

    # msg1 = ('Подписка', 'Подвердите пожалуйста подписку',
    #         'subscribe@supersite.kz',
    #         ['user@otheruser.kz', 'megauser@megasite.kz']
    #         )
    # msg2 = ("Подписка", "Ваша подписка подтверждена",
    #         "subscribe@supersite.kz",
    #         ["user@otheruser.kz", "otheruser@megasite.kz"],
    #         )
    # send_mass_mail((msg1, msg2))

    # user = User.objects.get(username='admin')
    # user.email_user("Подъём!", "Admin, не спи!", fail_silently=True)

    # mail_managers("Подъём!", "Редакторы, не спите!",
    #               html_message='<strong>Редакторы, не спите!</strong>')

    return render(request, "testapp/test_email.html")


def hide_comment(request):
    if request.user.has_perm('testapp.hide_comments'):
        # пользвователь может скрывать комментарии
        pass

# Выводим данные первого пользователя
class FirstUserView(View):
    def get(self, request, *args, **kwargs):
        first_user = User.objects.order_by("id").first()
        if first_user:
            return JsonResponse(
                {
                    "id": first_user.id,
                    "username": first_user.username,
                    "email": first_user.email,
                    "date_joined": first_user.date_joined,
                }
            )
        return JsonResponse({"error": "No user found"}, status=404)

# Выводим данные всех пользователей
class AllUsersView(ListView):
    model = User
    context_object_name = "users"

    def render_to_response(self, context, **response_kwargs):
        users = list(context["users"].values("id", "username", "email", "date_joined"))
        return JsonResponse(users, safe=False, **response_kwargs) 

# Выводим данные о конкретном пользователе по запросу ID
class UserDetailView(DetailView):
    model = User

    def render_to_response(self, context, **response_kwargs):
        user = context["object"]
        return JsonResponse(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "date_joined": user.date_joined,
            },
            **response_kwargs
        )

# Вводим ID пользователя
class UserSearchView(FormView):
    template_name = "testapp/user_search.html"
    form_class = UserSearchForm

    def form_valid(self, form):
        user_id = form.cleaned_data["user_id"]
        return redirect(reverse("testapp:user_detail", kwargs={"pk": user_id}))


def test_filters_tags(request):
    data = {
        "username": "test_viewer",
        "balance": 12345.6789,
        "date_joined": now(),
        "text": " Текст для тестирования фильтров и тегов!",
        "items": ["овощи", "фрукты", "ягоды"]
    }

    return render(request, "testapp/test_filters_tags.html", data)


@api_view(['GET', 'POST'])
def api_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_user_detail(request, pk):
    user = User.objects.get(pk=pk)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



    
