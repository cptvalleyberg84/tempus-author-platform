from django.urls import path
from .views import BlogListView, PostDetailView
from . import views


urlpatterns = [
    path('', BlogListView.as_view(), name='blog'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('<slug:post_slug>/comment/<int:comment_id>/edit/',
         views.comment_edit,
         name='comment_edit'),
    path('<slug:post_slug>/comment/<int:comment_id>/delete/',
         views.comment_delete,
         name='comment_delete'),
]
