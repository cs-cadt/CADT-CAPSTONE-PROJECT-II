from django.urls import path
from .views import ChatbotAPI
urlpatterns = [
    path('response/', ChatbotAPI.as_view(), name='chatbotapi'),
]
