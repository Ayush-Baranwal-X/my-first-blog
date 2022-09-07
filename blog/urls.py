from django.urls import path
from . import views

urlpatterns = [
    path('', views.postList, name='post_list'),
    path('post/<int:pk>/', views.postDetail, name='post_detail'),
    path('post/new', views.postNew, name='post_new'),
    path('post/edit/<int:pk>', views.postEdit, name='post_edit')
]
