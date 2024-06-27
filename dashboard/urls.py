from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.index, name= 'dashboard-index'),
    path('staff/', views.staff, name= 'dashboard-staff'),
    path('staff/detail/<int:pk>/', views.staff_detail, name= 'dashboard-staff-detail'),
    path('product/', views.product, name= 'dashboard-product'),
    path('product/delete/<int:pk>/', views.product_delete, name= 'dashboard-product-delete'),
    path('product/update/<int:pk>/', views.product_update, name= 'dashboard-product-update'),
    path('order/', views.order, name= 'dashboard-order'),
    # code edit for approve and reject button but not working
    # path('order/approve/<int:pk>/', views.approve_order, name= 'dashboard-order-approve'),
    # path('order/reject/<int:pk>/', views.reject_order, name= 'dashboard-order-reject'),
]