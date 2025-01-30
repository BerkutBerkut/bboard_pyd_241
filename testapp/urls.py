from django.urls import path
from testapp.views import (SMSListView, test_cookie, 
                           FirstUserView, AllUsersView,
                           UserDetailView, UserSearchView)


app_name = 'testapp'

urlpatterns = [
    path('', test_cookie, name='test_cookie'),
    path('sms_list/', SMSListView.as_view(), name='sms_list'),

    path('first/', FirstUserView.as_view(), name='first_user'),
    path('users/', AllUsersView.as_view(), name='all_users'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user_search/', UserSearchView.as_view(), name='user_search'),

]