from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_list_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import FormView
from testapp.forms import UserSearchForm

from django.contrib.auth.models import User

from testapp.models import SMS


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
