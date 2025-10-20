from django.urls import path
from . import views # Importe suas views
from django.contrib.auth import views as auth_views # Importa views de autenticação

urlpatterns = [
    # Caminho para sua view de login
    path('login/', views.login_view, name='login'),
    
    # Caminho para logout (usa a view padrão do Django)
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    
    path ('register',views)
]