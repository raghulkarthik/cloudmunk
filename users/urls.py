from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),

    # path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # path('upload/', views.upload_file, name='upload_file'),
    # path('files/', views.view_files, name='file_list'),
    path('test-email/', views.test_email, name='test_email'),

]
