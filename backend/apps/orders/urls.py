from django.urls import path
from .views import OrderListCreateView, OrderDetailView, CouponValidateView, ShippingCostView, OrderInvoiceView

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='order-list-create'),
    path('<uuid:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('<uuid:pk>/invoice/', OrderInvoiceView.as_view(), name='order-invoice'),
    path('coupon/validate/', CouponValidateView.as_view(), name='coupon-validate'),
    path('shipping/cost/', ShippingCostView.as_view(), name='shipping-cost'),
]
