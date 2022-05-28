from django.urls import path, re_path
from . import views
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', views.getRoutes),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('customer/<int:id>/', views.customer), 
    path('create-customer/', views.create_customer), 
    path('rent-locations/', views.rent_locations), 
    path('car/', views.car), 
    path('allocate-car/<int:id>/', views.allocate_car), 
    re_path(r'^reservation/((?P<id>\d+)/)?$', views.reservation), 
    # path('reservation/', views.reservation), 
]
