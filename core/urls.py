from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    #path('account/', include('core.urls.')),
    path('home/',views.index, name='home'),
    #path('',views.index, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:home'), name='logout'),
    path('u/<str:username>/', views.ProfileView, name='profile'),
    path('u/<str:username>/update', views.update_profile, name='profile-update'),
    path('temp/',views.temp, name='temp'),
    path('u/<str:username>/follow', views.follow, name='follow'),
    path('u/<str:username>/create_post',views.create_post,name='create_post'),
    path('u/<str:username>/<int:post_id>/create_comment',views.create_comment,name='create_comment'),
]