from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('register/', views.register, name='register'),
    path('checkout/', views.checkout, name='checkout'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:id>/<str:action>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.my_orders, name='my_orders'), 
    path('order-success/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('tracking/', views.tracking, name='tracking'),
    path('checkout/', views.checkout, name='checkout'),
    path('faq/', views.faq, name='faq'),
    path('inquiries/', views.inquiries, name='inquiries'),
    path('mark-replied/<int:id>/', views.mark_replied, name='mark_replied'),
    
 
]