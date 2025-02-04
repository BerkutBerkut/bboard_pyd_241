from django.urls import path
from testapp.views import (SMSListView, test_cookie, test_email, 
                           FirstUserView, AllUsersView,
                           UserDetailView, UserSearchView, 
                           test_filters_tags)


app_name = 'testapp'

urlpatterns = [
    path("cookie/", test_cookie, name="test_cookie"),
    path("email/", test_email, name="test_email"),
    path("sms_list/", SMSListView.as_view(), name="sms_list"),
    path("first/", FirstUserView.as_view(), name="first_user"),
    path("users/", AllUsersView.as_view(), name="all_users"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("user_search/", UserSearchView.as_view(), name="user_search"),
    path("test_filters_tags/", test_filters_tags, name="test_filters_tags")
]
