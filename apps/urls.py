from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/', views.index, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('product/', views.product, name='product'),
    path('product/addproduct/', views.create_product, name='add_product'),
    path('product/updateproduct/<int:id>/', views.update_product, name='update_product'),
    path('product/deleteproduct/<int:id>/', views.delete_product, name='delete_product'),
    path('event/', views.event, name='event'),
    path('event/addevent/', views.create_event, name='add_event'),
    path('event/updateevent/<int:id>/', views.update_event, name='update_event'),
    path('event/deleteevent/<int:id>/', views.delete_event, name='delete_event'),
    path('payment/', views.payment_method, name='payment'),
    path('payment/addpayment/', views.create_payment_method, name='add_payment'),
    path('payment/updatepayment/<int:id>/', views.update_payment_method, name='update_payment'),
    path('payment/deletepayment/<int:id>/', views.delete_payment_method, name='delete_payment'),
    path('invoice/', views.invoice, name='invoice'),
    path('invoice/addinvoice/', views.create_invoice, name='add_invoice'),
    path('invoice/updateinvoice/<int:id>/', views.update_invoice, name='update_invoice'),
    path('invoice/viewinvoice/<int:id>/', views.view_invoice, name='view_invoice'),
    path('invoice/deleteinvoice/<int:id>/', views.delete_invoice, name='delete_invoice'),
    path('prediction/', views.prediction_page, name='prediction'),
    path('predict/', views.prediction, name='predict'),

    
]