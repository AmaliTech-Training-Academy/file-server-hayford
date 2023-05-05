from django.urls import path
from . import views

app_name = 'filesystem'

urlpatterns = [
    path('', views.home.as_view(), name="home"),
    path('uploads/', views.upload, name="upload"),
    # path('files/', views.FileListView.as_view(), name='upload_list'),
]
