from django.urls import path
from .views import FormDetailView, FormDeleteView, FormUpdateView
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('form/search/', views.search_form, name="search"),
    path('form/<int:pk>/', FormDetailView.as_view(), name="form-detail"),
    path('form/<int:pk>/delete/', FormDeleteView.as_view(), name="form-delete"),
    path('form/<int:pk>/update/', FormUpdateView.as_view(), name="form-update"),
    path('form/new/', views.form, name="form-create")
]
