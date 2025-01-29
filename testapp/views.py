from django.shortcuts import render
from django.views.generic import ListView
from testapp.models import SMS

# Create your views here.

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

    

