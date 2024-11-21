from django.urls import path
from .views import dashboard
from . import views

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('email/status/', views.email_status_webhook, name='email_status_webhook'),
    
]
