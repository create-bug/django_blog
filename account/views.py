from django.shortcuts import render, HttpResponse
#from django.contrib.auth import authenticate, login
#from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, userRegistrationForm
# Create your views here.

@login_required
def test_login(request):
    return render(request, 'account/test_login.html', {'section':'test_login'})

def register(request):
    if request.method == 'POST':
        user_form =  userRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user':new_user})
    else:
        user_form = userRegistrationForm()

    return render(request, 'account/register.html',{'user_form':user_form})