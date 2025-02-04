from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from datetime import date

# expenses/views.py
from django.shortcuts import render
from .models import Expense

def expense_list(request):
    expenses = Expense.objects.all().order_by('-date')
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})




