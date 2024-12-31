from django.urls import path, include
from . import views
# from rest_framework import routers
# router = routers.DefaultRouter()

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LogIn.as_view(), name='login'),
    path('register/', views.RegisterClient.as_view(), name='register'),
    path('logout/', views.logout, name='logout'),
    # path('ambersignal/', include(router.urls)),    
]
