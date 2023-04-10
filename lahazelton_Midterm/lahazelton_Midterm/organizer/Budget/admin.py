from django.contrib import admin
from Budget.models import Budget, BudgetCategory
from Tasks.models import Task, TaskCategory
# Register your models here.
admin.site.register(TaskCategory)
admin.site.register(BudgetCategory)
