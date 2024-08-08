from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    # path('', include('admin_adminlte.urls')),
    path("api/",include("auths.urls")),
    path("api/",include("secretkey.urls")),
    path("api/",include("chatbotapi.urls")),
    path("api/",include("managedata.urls")),
    path("api/",include("managemodel.urls")),
    path("api/", include("monitoring.urls")),
    path("", include("admin_board.urls")),
    path("", include("user_chatbot.urls")),
]
