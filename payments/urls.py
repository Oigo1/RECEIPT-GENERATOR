from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.payment_form, name='payment_form'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'), # Register page
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'), # Logout
]