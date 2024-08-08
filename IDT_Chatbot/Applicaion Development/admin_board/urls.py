from django.urls import path
from .views import ChangeModelView, edit_model_view, train_model_view, delete_model_view, edit_secret_key, edit_file_view, dataset_view, upload_file_view, delete_file_view, admin_login, admin_dashboard, forgot_password_view, verify_code_view, reset_password_view, manage_secret_keys_view, generate_key, models_view, model_upload, delete_secret_key
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin_login, name='login'),
    path('forgot/', forgot_password_view, name='forgot_password'),
    path('verify/', verify_code_view, name='verify_code'),
    path('reset/', reset_password_view, name='reset_password'),
    #admin dashboard path
    path('admin/dashboard/', admin_dashboard, name='dashboard'),
    #secretkeys path
    path('secretkeys/', manage_secret_keys_view, name='manage_secret_key'),
    path('secretkeys/generatekey/', generate_key, name='generate_key'),  # generate secret key
    path('secretkey/<int:id>/', delete_secret_key, name='delete_secret_key'),
    path('secretkeys/edit/<int:key_id>/', edit_secret_key, name='edit_secret_key'),
    #models path
    path('models/', models_view, name='manage_models'),
    path('models/edit/<str:file_name>/', edit_model_view, name='edit_model'),
    path('models/upload/', model_upload, name='model_upload'),  # upload model file
    path('models/delete/<str:file_name>/', delete_model_view, name='delete_model'),
    path('models/train/', train_model_view, name='train_model'),
    path('models/change/', ChangeModelView.as_view(), name='change_model'),

    #dataset path
    path('dataset/', dataset_view, name='manage_dataset'),
    path('dataset/edit/<str:file_name>/', edit_file_view, name='edit_dataset'),
    path('dataset/upload/', upload_file_view, name='upload_file'),
    path('dataset/delete/<str:file_name>/', delete_file_view, name='delete_file'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
