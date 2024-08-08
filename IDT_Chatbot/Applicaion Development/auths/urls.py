from django.urls import path
from . import views
from .views import Auths,ForgotPasswordAPI,ResetPasswordAPI,VerifyCodeAPI
urlpatterns = [
    path('auth/login/', views.Auths.as_view(), name='login'),
    # path('auth/sendmail/', views.SendMailAPI.as_view(), name='sendmail'),
    path('auth/forgot/sendcode/',view=ForgotPasswordAPI.as_view(),name='forgot_password'),
    path('auth/forgot/verify/',view=VerifyCodeAPI.as_view(),name='verify_code'),
    path('auth/forgot/reset/',view=ResetPasswordAPI.as_view(),name='reset_password')
    
]
