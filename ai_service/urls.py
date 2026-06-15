"""
AI Service URLs
"""
from django.urls import path
from . import views

app_name = 'ai_service'

urlpatterns = [
    path('ask/', views.ai_ask, name='ai_ask'),
    path('inventory-insights/', views.ai_inventory_insights, name='ai_inventory_insights'),
    path('status/', views.ai_status, name='ai_status'),
]
