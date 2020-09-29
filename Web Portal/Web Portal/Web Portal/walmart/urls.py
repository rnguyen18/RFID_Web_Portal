from django.urls import path
from .views import FormDetailView
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('form/<int:pk>/', FormDetailView.as_view(), name="detail"),
    path('form/new/', views.form, name="form")
]