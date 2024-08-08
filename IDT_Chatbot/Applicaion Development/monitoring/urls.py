from django.urls import path
from .views import UnAnsweredAPI,QuestionMonitorAPI
urlpatterns = [
    path('monitoring/unanswered/', UnAnsweredAPI.as_view(), name='unanswered'),
    path('monitoring/numbers/', QuestionMonitorAPI.as_view(), name='numbers'),
]
