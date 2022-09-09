from django.urls import path
from . import views

urlpatterns = [
    path('', views.postList, name='post_list'),
    path('post/new/', views.postNew, name='post_new'),
    path('post/<int:pk>/', views.postDetail, name='post_detail'),
    path('post/edit/<int:pk>/', views.postEdit, name='post_edit'),
    path('post/delete/<int:pk>/', views.postDelete, name='post_delete'),
    path('post/publish/<int:pk>/', views.postPublish, name='post_publish'),
    path('drafts/', views.postDrafts, name='post_drafts'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
]
