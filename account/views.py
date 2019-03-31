from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm
# Create your views here.

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('登录成功')
                else:
                    return HttpResponse('登录失败')
            else:
                return HttpResponse('登录失败')
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form':form})