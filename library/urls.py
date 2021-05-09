from library.models import Payment_bill, Seller_inventory
from django.urls import path
from django.urls.conf import path 
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name = 'place_order/'),
    path('enter_order_specs/', views.enter_order_specs,name='enter_order_specs'),

    path('show_books/',views.show_books, name='show_books'),
    path('upd_inventory/',views.upd_inventory, name='upd_inventory'),
    path('payment_details/',views.payment_details,name='payment_details'),
    path('print_college_users/',views.print_college_users,name='print_college_users')
]