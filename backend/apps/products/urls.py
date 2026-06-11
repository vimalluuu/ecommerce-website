from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'', ProductViewSet, basename='product')

urlpatterns = [
    path('<uuid:product_id>/reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-reviews'),
    path('<uuid:product_id>/reviews/<uuid:pk>/', ReviewViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='product-review-detail'),
    path('', include(router.urls)),
]
