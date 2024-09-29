from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<str:category_name>/', views.category_expenses, name='category_expenses'),
    path('reset/', views.reset_expenses, name='reset_expenses'),  
]   