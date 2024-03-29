from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import ExpenseForm,IncomeForm
from .models import Expense,Income
import datetime
from django.db.models import Sum
# Create your views here.
def index(request):
    if request.method == "POST":
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()

    expenses = Expense.objects.all()
    total_expenses = expenses.aggregate(Sum('amount'))

    # Logic to calculate 365 days expenses
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    yearly_expenses = Expense.objects.filter(date__gt=last_year)
    yearly_sum = yearly_expenses.aggregate(Sum('amount'))

    # Logic to calculate 30 days expenses
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    monthly_expenses = Expense.objects.filter(date__gt=last_month)
    monthly_sum = monthly_expenses.aggregate(Sum('amount'))

    # Logic to calculate 7 days expenses
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    weekly_expenses = Expense.objects.filter(date__gt=last_week)
    weekly_sum = weekly_expenses.aggregate(Sum('amount'))

    daily_sums = Expense.objects.filter().values('date').order_by('date').annotate(sum=Sum('amount'))

    categorical_sums = Expense.objects.filter().values('category').order_by('category').annotate(sum=Sum('amount'))
    print(categorical_sums)

    # Calculate savings 
    user_income = request.COOKIES.get('userIncome')
    user_income = float(user_income) if user_income else 0.0

    monthly_expenses_sum = monthly_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    savings = user_income - monthly_expenses_sum

    is_negative_savings = savings < 0

    expense_form = ExpenseForm()
    return render(request, 'myapp/index.html', {'expense_form': expense_form, 'expenses': expenses,'total_expenses': total_expenses, 'yearly_sum': yearly_sum,'weekly_sum': weekly_sum, 'monthly_sum': monthly_sum,'daily_sums': daily_sums, 'categorical_sums': categorical_sums,'savings': savings,'is_negative_savings': is_negative_savings})

def edit(request,id):
    expense = Expense.objects.get(id=id)
    expense_form = ExpenseForm(instance=expense)
    if request.method =="POST":
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(request.POST,instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')
        
    return render(request,'myapp/edit.html',{'expense_form':expense_form})

def delete(request,id):
    if request.method =='POST' and 'delete' in request.POST:
        expense = Expense.objects.get(id=id)
        expense.delete()
    return redirect('index')
from django.http import HttpResponse
