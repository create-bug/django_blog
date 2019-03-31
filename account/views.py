from django.shortcuts import render, HttpResponse
#from django.contrib.auth import authenticate, login
#from .forms import LoginForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def test_login(request):
    return render(request, 'account/test_login.html', {'section':'test_login'})