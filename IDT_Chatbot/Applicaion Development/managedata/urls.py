from django.urls import path
from .views import UploadFileAPI,downloadFileAPI
urlpatterns = [
    path('data', UploadFileAPI.as_view(), name='upload_file'),
    path('data/download', downloadFileAPI.as_view(), name='download_file'),
    
]
