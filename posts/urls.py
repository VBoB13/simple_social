from django.urls import path, include

from . import views

app_name = 'posts'

comment_patterns = [
    path('create/', views.create_comment, name='comment_create'),
]

post_patterns = [
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/comments/', include(comment_patterns)),
]

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.posts_login, name='login'),
    path('logout/', views.posts_logout, name='logout'),
    path('post/', include(post_patterns)),
]
