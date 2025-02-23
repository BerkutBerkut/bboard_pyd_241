from django.urls import path
from django.views.decorators.cache import cache_page
from testapp.views import (SMSListView, test_cookie, test_email, 
                           FirstUserView, AllUsersView,
                           UserDetailView, UserSearchView, 
                           test_filters_tags, api_users, api_view,
                           api_user_detail)


app_name = 'testapp'

urlpatterns = [
    path('api/users/<int:pk>/', api_user_detail),
    path('api/users/', api_users),
    path("cookie/", test_cookie, name="test_cookie"),
    path("email/", test_email, name="test_email"),
    path("sms_list/", SMSListView.as_view(), name="sms_list"),
    path("first/", FirstUserView.as_view(), name="first_user"),
    path("users/", AllUsersView.as_view(), name="all_users"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("user_search/", UserSearchView.as_view(), name="user_search"),
    path("test_filters_tags/", test_filters_tags, name="test_filters_tags")
]
