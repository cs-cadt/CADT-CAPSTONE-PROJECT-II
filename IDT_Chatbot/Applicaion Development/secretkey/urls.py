from django.urls import path
from .views import SecretKeyAPI
urlpatterns = [
    path('secretkey/',SecretKeyAPI.as_view(),name='secretkey')
]
