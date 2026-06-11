from rest_framework import viewsets, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from apps.products.models import Product, Category
from apps.orders.models import Order, Coupon
from apps.products.serializers import ProductSerializer, CategorySerializer
from apps.orders.serializers import OrderSerializer, CouponSerializer

User = get_user_model()

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin)

class AdminDashboardStatsView(views.APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)
        
        total_revenue = Order.objects.filter(payment_status='paid').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        total_orders = Order.objects.count()
        total_users = User.objects.count()
        total_products = Product.objects.count()

        recent_orders = OrderSerializer(Order.objects.order_by('-created_at')[:5], many=True).data
        
        top_products = Product.objects.annotate(
            orders_count=Count('orderitem')
        ).order_by('-orders_count')[:5]
        
        return Response({
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'total_users': total_users,
            'total_products': total_products,
            'recent_orders': recent_orders,
            'top_products': ProductSerializer(top_products, many=True).data
        })

class AdminProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'id'

class AdminCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'slug'

class AdminOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'id'

from rest_framework import generics

class AdminUserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        users = User.objects.annotate(orders_count=Count('order')).values(
            'id', 'name', 'email', 'phone', 'is_admin', 'created_at', 'orders_count'
        )
        return Response(list(users))

class AdminAnalyticsView(views.APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        # Simplified analytics data
        return Response({
            'revenue_by_month': [], # Mocked or implement later
            'orders_by_status': list(Order.objects.values('order_status').annotate(count=Count('id'))),
            'top_categories': list(Category.objects.annotate(sales=Count('product__orderitem')).values('name', 'sales').order_by('-sales')[:5])
        })

class AdminCouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
