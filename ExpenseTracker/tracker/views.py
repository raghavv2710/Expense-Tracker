from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
from django.db.models import Sum
import matplotlib.pyplot as plt
import io
import urllib, base64
from collections import defaultdict

# Function to generate the expense chart
def generate_expense_chart(grouped_expenses):
    # Prepare the data for the chart
    categories = list(grouped_expenses.keys())
    total_amounts = [sum(expense.amount for expense in expenses) for expenses in grouped_expenses.values()]

    # Create the bar chart
    plt.figure(figsize=(8, 4))
    plt.bar(categories, total_amounts, color='skyblue')
    plt.xlabel('Categories')
    plt.ylabel('Total Amount')
    plt.title('Total Expenses by Category')

    # Make the x labels horizontal
    plt.xticks(rotation=0)

    # Convert the plot to a PNG image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode the PNG image to base64
    image_base64 = base64.b64encode(image_png).decode('utf-8')

    # Return the image as a base64 string
    return image_base64


# Home view
def home(request):
    expenses = Expense.objects.all()
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # Handle form submission
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ExpenseForm()

    # Get all distinct categories
    categories = [expense['category'] for expense in expenses.values('category').distinct()]

    # Filtering based on selected category
    selected_category = request.GET.get('category')

    # Show all expenses if "all" is selected, or no expenses if nothing is selected
    if selected_category == "all":
        filtered_expenses = expenses
    elif selected_category:
        filtered_expenses = expenses.filter(category=selected_category)
    else:
        filtered_expenses = Expense.objects.none()  # No expenses displayed if nothing is chosen

    # Grouping expenses by category for the chart
    grouped_expenses = defaultdict(list)
    for expense in expenses:
        grouped_expenses[expense.category].append(expense)

    # Generate the chart for expenses
    chart = generate_expense_chart(grouped_expenses)

    return render(request, 'tracker/home.html', {
        'expenses': expenses,
        'total_expense': total_expense,
        'form': form,
        'filtered_expenses': filtered_expenses,
        'grouped_expenses': grouped_expenses,
        'categories': categories,
        'chart': chart,
    })


# View to reset all expenses
def reset_expenses(request):
    if request.method == 'POST':
        # Delete all expenses
        Expense.objects.all().delete()
        return redirect('home')

    return redirect('home')  # Redirect to home if accessed via GET


# View for category-specific expenses
def category_expenses(request, category_name):
    expenses = Expense.objects.filter(category=category_name)
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'tracker/category_expenses.html', {
        'expenses': expenses,
        'total_expense': total_expense,
        'category_name': category_name,
    })
