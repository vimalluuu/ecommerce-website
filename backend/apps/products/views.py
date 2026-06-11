from rest_framework import viewsets, generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer
from .filters import ProductFilter

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).prefetch_related('reviews', 'category')
    serializer_class = ProductSerializer
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'tags']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_products = self.queryset.filter(is_featured=True)[:8]
        serializer = self.get_serializer(featured_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def related(self, request, id=None):
        product = self.get_object()
        related = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]
        serializer = self.get_serializer(related, many=True)
        return Response(serializer.data)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return Review.objects.filter(product_id=product_id)

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        serializer.save(user=self.request.user, product_id=product_id)
