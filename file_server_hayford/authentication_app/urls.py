from django.urls import path
from . import views

app_name = 'authentication_app'

urlpatterns = [
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='account_activate'),
    path('reset/<uidb64>/<token>', views.reset_password_confirm, name='password_reset_confirm'),
    path('password_reset/', views.password_reset, name='reset_page'),
    path('password_reset/done/', views.resetPageDone, name='reset_page_done'),
]