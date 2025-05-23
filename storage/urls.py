from django.urls import path
from . import views
app_name = 'storage'

urlpatterns = [
    path('upload/', views.storage_upload_file, name='upload_file'),
    path('files/', views.storage_file_list, name='file_list'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('test-email/', views.test_email, name='test_email'),
]   
