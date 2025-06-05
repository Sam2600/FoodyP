from . import views
from django.urls import path

urlpatterns = [

    # ✅ Terms
    path('terms/', views.terms, name='terms'),

    # ✅ View list items
    path('', views.item_list, name='item_list'),

    # ✅ View order_success
    path('order_success/', views.order_success, name='order_success'),

    # ✅ Privacy
    path('privacy/', views.privacy, name='privacy'),

    # ✅ View cart items
    path('checkout/', views.checkout, name='checkout'),

    # ✅ About us page
    path('about-us/', views.about_us, name='about_us'),

    # ✅ Disclaimer
    path('disclaimer/', views.disclaimer, name='disclaimer'),

    # ✅ Contact us page
    path('contact-us/', views.contact_us, name='contact_us'),

    # ✅ Update ordered items count
    path('update-cart/', views.update_cart, name='update_cart'),

    # ✅ View ordered items
    path('place-order/', views.place_order, name='place_order'),

    # ✅ Add to session
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
]
