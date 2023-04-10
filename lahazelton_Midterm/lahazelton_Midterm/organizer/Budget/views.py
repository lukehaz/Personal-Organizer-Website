from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from Budget.models import Budget, BudgetCategory
from Budget.form import BudgetEntryForm
# Create your views here.
@login_required(login_url='/login/')
def edit(request, id):
	if (request.method == "GET"):
		bEntry = Budget.objects.get(id=id)
		bform = BudgetEntryForm(instance=bEntry)
		context = {"form_data": bform}
		return render(request, 'budget/edit.html', context)
	elif (request.method == "POST"):
		if ("edit" in request.POST):
			bform = BudgetEntryForm(request.POST)
			if (bform.is_valid()):
				bEntry = bform.save(commit=False)
				bEntry.user = request.user
				bEntry.id = id
				bEntry.save()
				return redirect("/budget/")
			else:
				context = {
                    "form_data": bform
				}
				return render(request, 'budget/add.html', context)
		else:
			return redirect("/budget/")

@login_required(login_url = '/login/')
def home(request):
	if(BudgetCategory.objects.count() == 0):
		BudgetCategory(category = "Food").save()
		BudgetCategory(category = "Clothing").save()
		BudgetCategory(category = "Housing").save()
		BudgetCategory(category = "Education").save()
		BudgetCategory(category = "Entertainment").save()
		BudgetCategory(category = "Other").save()

	if(request.method == "GET" and "delete" in request.GET):
		id = request.GET["delete"]
		Budget.objects.filter(id=id).delete()
		return redirect("/budget/")
	else:
		table_data = Budget.objects.filter(user = request.user)
		aBudget = 0
		pBudget = 0
		for budget in table_data:
			pBudget += budget.projected
			aBudget += budget.actual
		change = aBudget - pBudget
		context = {"table_data": table_data,"finalValue": change}
	return render(request, 'budget/budget.html', context)

@login_required(login_url = '/login/')
def add(request):
    if(request.method == 'POST'):
        if("add" in request.POST):
            bform = BudgetEntryForm(request.POST)
            if(bform.is_valid()):
                projected = bform.cleaned_data["projected"]
                category = bform.cleaned_data["category"]
                description = bform.cleaned_data["description"]
                actual = bform.cleaned_data["actual"]
                user = User.objects.get(id=request.user.id)
                Budget(user=user, description=description, category=category, projected=projected, actual=actual).save()
                return redirect("/budget/")
            else:
                context = {
                    "form_data": bform
                }
                return render(request, 'budget/add.html', context)
        else:
            return redirect("/budget/")
    else:
        context = {
            "form_data": BudgetEntryForm()
        }
        return render(request, 'budget/add.html', context)
