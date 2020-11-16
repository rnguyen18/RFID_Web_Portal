from django.urls import path
from .views import FormDetailView, FormPDFView
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('form/search/', views.search_form, name="search"),
    path('form/<int:pk>/', FormDetailView.as_view(), name="form-detail"),
    path('form/<int:pk>/pdf/', FormPDFView.as_view(), name="form-pdf"),
    path('form/new/', views.form, name="form-create")
]
