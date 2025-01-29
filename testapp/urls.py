from django.urls import path
from testapp.views import SMSListView, test_cookie


app_name = 'testapp'

urlpatterns = [
    path('', test_cookie, name='test_cookie'),
    path('sms_list/', SMSListView.as_view(), name='sms_list')

]