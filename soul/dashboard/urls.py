from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='dashboard'),
    path('add', views.add, name='add'),
    path('getData',views.getData, name='getData')
]
