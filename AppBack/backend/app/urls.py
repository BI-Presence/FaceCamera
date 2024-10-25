from django.urls import path
from app import views
from .views import add_employee, train_model_view

urlpatterns = [
    path('', views.index, name="index"),
    path('about', views.about, name="about"),
    path('login', views.login, name="login"),
    #path('add_employee/', add_employee, name='add_employee'),
    path('add_employee/', add_employee, name='add_user'),
    path('train_data', views.train_data, name='train_data'),
    path('train_model/', train_model_view, name='train_model'),
    path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('logout/', views.logout, name='logout'),
]
