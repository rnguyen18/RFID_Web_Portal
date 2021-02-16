from django.urls import path
from .views import FormDetailView, FormPDFView, FormEditView
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('form/view/', views.view_form, name="view"),
    path('form/view/<int:pk>/', FormDetailView.as_view(), name="form-detail"),
    path('form/view/<int:pk>/edit', FormEditView.as_view(), name="form-edit"),
    path('form/view/<int:pk>/pdf/', FormPDFView.as_view(), name="form-pdf"),
    path('form/new/', views.form, name="form-create"),
    path('contactUs', views.contactUs, name="contactUs")
]
