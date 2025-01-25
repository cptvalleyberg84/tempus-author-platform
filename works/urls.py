from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_works, name='works'),
    path('<int:work_id>/', views.work_detail, name='work_detail'),
]
