from django.urls import path
from . import views

app_name = 'filesystem'

urlpatterns = [
    path('upload_file/', views.upload_file, name='upload_file'),
    path('download_file/<int:file_id>', views.download_file, name='download_file'),
    path('send_file/<int:file_id>', views.send_file_email, name='send_file_email'),
    path('files/', views.FileListView.as_view(), name='upload_list'),
    path('files/<int:pk>/', views.FileDetailView.as_view(), name='file_detail'),
    path('files/delete/<int:pk>/', views.delete_upload_file, name='delete_file'),
    path('search/', views.search_view, name='search'),
    path('logs/', views.log, name='logs'),
    path('preview/<int:file_id>/', views.preview, name='preview'),
    path('display/<int:file_id>/', views.open_page, name='open_page'),
]
