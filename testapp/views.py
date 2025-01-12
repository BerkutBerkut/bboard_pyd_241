from django.shortcuts import render
from django.views.generic import ListView
from testapp.models import SMS

# Create your views here.

class SMSListView(ListView):
    model = SMS
    template_name = 'testapp/sms_list.html'
    context_object_name = 'sms_list'
    ordering = ['-timestamp']

    

