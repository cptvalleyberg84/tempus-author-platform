from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('user/<int:user_id>/', views.public_profile, name='public_profile'),
    path(
        'order_history/<order_id>',
        views.order_history,
        name='order_history'
    ),
]
