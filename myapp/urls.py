from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('create/',views.product_create, name='product_create'),
    path('update/<int:pk>', views.product_update, name='product_update'),
    path('delete/<int:pk>', views.product_delete, name='product_delete'),
    path('login/', auth_views.LoginView.as_view(template_name = 'myapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile' ),
    path('dashboard/', views.dashboard, name='dashboard'),
    
]