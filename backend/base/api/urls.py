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
    path('all-reservations/', views.all_reservations), 
    path('all-rents/', views.all_rents), 
    path('customers/', views.customers), 
    path('statistics/', views.statistics), 
    re_path(r'^car-crud/((?P<id>\d+)/)?$', views.car_crud), 
    path('rent/', views.rent), 
    path('allocate-car/<int:id>/', views.allocate_car), 
    path('deallocate-car/<int:id>/', views.deallocate_car), 
    re_path(r'^reservation/((?P<id>\d+)/)?$', views.reservation), 
    # path('reservation/', views.reservation), 
]
