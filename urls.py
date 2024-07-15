from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('loginpage/', views.loginpage, name='loginpage'),
    path("login/",auth_views.LoginView.as_view(template_name='login.html'),name="login"),
    path('logout/',views.logout_page,name="logout"),
    path('register/', views.register, name='register'),
    path("profile/",views.profile,name="profile"),
    path('loginpage/<str:name>', views.loginpageview, name='loginpage'),
    path('addtocart',views.add_to_cart,name="addtocart"),
    path('cart',views.cart_page,name="cart"),
    path('remove_cart/<str:cid>',views.remove_cart,name="remove_cart"),

    

] 
