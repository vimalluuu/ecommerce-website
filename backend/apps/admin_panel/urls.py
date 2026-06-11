from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdminDashboardStatsView, AdminProductViewSet, AdminCategoryViewSet,
    AdminOrderViewSet, AdminUserListView, AdminAnalyticsView, AdminCouponViewSet
)

router = DefaultRouter()
router.register(r'products', AdminProductViewSet, basename='admin-product')
router.register(r'categories', AdminCategoryViewSet, basename='admin-category')
router.register(r'orders', AdminOrderViewSet, basename='admin-order')
router.register(r'coupons', AdminCouponViewSet, basename='admin-coupon')

urlpatterns = [
    path('dashboard/', AdminDashboardStatsView.as_view(), name='admin-dashboard'),
    path('users/', AdminUserListView.as_view(), name='admin-users'),
    path('analytics/', AdminAnalyticsView.as_view(), name='admin-analytics'),
    path('', include(router.urls)),
]
