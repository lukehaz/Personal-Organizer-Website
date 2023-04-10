from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from Tasks.models import Task, TaskCategory
from Tasks.forms import TaskEntryForm
# Create your views here.
@login_required(login_url = '/login/')
def add(request):
    if(request.method == 'POST'):
        if("add" in request.POST):
            aform = TaskEntryForm(request.POST)
            if(aform.is_valid()):
                description = aform.cleaned_data["description"]
                category = aform.cleaned_data["category"]
                user = User.objects.get(id=request.user.id)
                Task(user=user, description=description, category=category).save()
                return redirect("/tasks/")
            else:
                context = {"form_data": aform}
                return render(request, 'tasks/add.html', context)
        else:
            return redirect("/tasks/")
    else:
        context = {
            "form_data": TaskEntryForm()
        }

        return render(request, 'tasks/add.html', context)

@login_required(login_url='/login/')
def edit(request, id):
	if (request.method == "GET"):
		taskEntry = Task.objects.get(id=id)
		eform = TaskEntryForm(instance=taskEntry)
		context = {"form_data": eform}
		return render(request, 'tasks/edit.html', context)
	elif (request.method == "POST"):
		if ("edit" in request.POST):
			eform = TaskEntryForm(request.POST)
			if (eform.is_valid()):
				taskEntry = eform.save(commit=False)
				taskEntry.user = request.user
				taskEntry.id = id
				taskEntry.save()
				return redirect("/tasks/")
			else:
				context = {"form_data": eform}
				return render(request, 'tasks/add.html', context)
		else:
			return redirect("/tasks/")

@login_required(login_url='/login/')
def completed(request, id):
    if(request.method == "GET"):
        taskEntry = Task.objects.get(id=id)
        taskEntry.is_completed = not taskEntry.is_completed
        taskEntry.save()
        return redirect("/tasks/")

@login_required(login_url = '/login/')
def home(request):
    if(TaskCategory.objects.count() == 0):
        TaskCategory(category = "School").save()
        TaskCategory(category = "Work").save()
        TaskCategory(category = "Home").save()
        TaskCategory(category = "Self Improvement").save()
        TaskCategory(category = "Other").save()

    if(request.method == "GET" and "delete" in request.GET):
        id = request.GET["delete"]
        Task.objects.filter(id=id).delete()
        return redirect("/tasks/")
    else:
        table_data = Task.objects.filter(user = request.user)
        context = {
            "table_data": table_data
        }
    return render(request, 'tasks/tasks.html', context)
