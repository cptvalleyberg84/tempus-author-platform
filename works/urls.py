from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_works, name='works'),
    path('<int:work_id>/', views.work_detail, name='work_detail'),
    path('bookcart/', views.view_bookcart, name='view_bookcart'),
    path('add/<int:work_id>/', views.add_to_bookcart, name='add_to_bookcart'),
    path(
        'adjust/<int:work_id>/',
        views.adjust_bookcart,
        name='adjust_bookcart'
    ),
    path(
        'remove/<int:work_id>/',
        views.remove_from_bookcart,
        name='remove_from_bookcart'
    ),
    path('add_review/<int:work_id>/', views.add_review, name='add_review'),
]
