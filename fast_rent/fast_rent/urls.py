from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('car_rent.urls')),
    path('api/', include('car_rent.api.urls')),
    path('admin/', admin.site.urls)
]
