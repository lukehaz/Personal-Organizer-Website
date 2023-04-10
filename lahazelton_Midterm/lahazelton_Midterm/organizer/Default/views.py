from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from Budget.models import Budget
from Tasks.models import Task
from Default.forms import LoginForm, JoinForm
# Create your views here.

def join(request):
    if (request.method == "POST"):
        jform = JoinForm(request.POST)
        if (jform.is_valid()):
            N_user = jform.save()
            N_user.set_password(N_user.password)
            N_user.save()
            return redirect("/")
        else:
            page_data = { "join_form": jform }
            return render(request, 'Organizer/join.html', page_data)
    else:
        jform = JoinForm()
        page_data = { "join_form": jform }
        return render(request, 'Organizer/join.html', page_data)

def user_login(request):
    if (request.method == 'POST'):
        lform = LoginForm(request.POST)
        if lform.is_valid():
            username = lform.cleaned_data["username"]
            password = lform.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    return redirect("/")
                else:
                    return HttpResponse("This account is not active.")
            else:
                print("Login Failed.")
                print("Used username: {} and password: {}".format(username,password))
                return render(request, 'Organizer/login.html', {"login_form": LoginForm})
    else:
        return render(request, 'Organizer/login.html', {"login_form": LoginForm})

@login_required(login_url = '/login/')
def home(request):
    bdata = Budget.objects.filter(user = request.user)
    tdata = Task.objects.filter(user = request.user)
    plist = []
    alist = []
    for bg in bdata:
        plist.append(bg.projected)
        alist.append(bg.actual)

    ccount = 0
    ucount = 0
    for t in tdata:
        if t.is_completed:
            ccount += 1
        else:
            ucount += 1

    tasksL = [ccount, ucount]
    pdata = { "budget_projected_data": plist,"budget_actual_data": alist,"task_data": tasksL}
    return render(request, 'default/home.html', pdata)

def user_logout(request):
    logout(request)
    return redirect("/")

def about(request):
    return render(request, 'Organizer/about.html')
