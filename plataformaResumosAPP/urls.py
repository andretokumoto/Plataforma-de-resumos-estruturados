from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

urlpatterns = [

   # path('login/', views.login_view, name='login'),
    path ('register/',views.register)
  #  path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout')
]