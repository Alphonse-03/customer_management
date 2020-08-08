from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home,name="home"),
    path('customer_profile/', views.customer_profile,name="customer_profile"),
    path('products/', views.products,name="products"),
    path('customer/<str:pk>/', views.customer,name="customer"),
    path('create_order/', views.create_order,name="create_order"),
    path('create_product/', views.create_product,name="create_product"),
    path('products/<str:pk>/delete', views.delete_product,name="view_product"),
    path('products/<str:pk>/edit', views.update_product,name="update_product"),
    path('order/<str:pk>/delete', views.delete_order,name="delete_order"),
    path('order/<str:pk>/edit', views.update_order,name="update_order"),
    path('customer/<str:pk>/delete', views.delete_customer,name="delete_customer"),
    path('update_customer/<str:pk>/edit', views.update_customer,name="update_customer"),
    path('customer/', views.create_customer,name="create_customer"),
    path('login/', views.login_page,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('user_profile/',views.user_profile,name="user_profile"),
    path('registration/', views.registration_page,name="registration"),
    path('create_order_customer/<str:pk>/', views.create_order_customer,name="create_order_customer"), 

    path('reset_password/',auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_send/',auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),


]
