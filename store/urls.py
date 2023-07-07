from django.urls import path
from . import views

urlpatterns = [
        path('', views.store_home, name='store_home'),  # Example URL pattern
        path('store/', views.store, name="store"),
        path('home/', views.home, name="home"),
        path('cart/', views.cart, name="cart"),
        path('checkout/', views.checkout, name="checkout"),
        path('update_item/', views.updateItem, name="update_item"),
        path('process_order/', views.processOrder, name="process_order"),
        path('product/<int:product_id>/', views.product_detail, name='product_detail'),
        path('register/', views.register, name="register"),

]