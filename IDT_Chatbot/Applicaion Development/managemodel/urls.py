from django.urls import path
from .views import ManageModelAPI,UploadModelAPI,TrainModelAPI,DeleteModelAPI,ChangeModelAPI,RunningModelAPI
urlpatterns = [
    path('model/manage', ManageModelAPI.as_view(), name='manage_model'),
    path('model/change', ChangeModelAPI.as_view(), name='change_model'),
    path('model/upload', UploadModelAPI.as_view(), name='upload_model'),
    path('model/delete', DeleteModelAPI.as_view(), name='delete_model'),
    path('model/training',TrainModelAPI.as_view(), name='train_model' ),
    path('model/running',RunningModelAPI.as_view(), name='running_model' ),
]
