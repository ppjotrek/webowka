from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('leki_app.urls')),
    path('admin/', admin.site.urls),
]
