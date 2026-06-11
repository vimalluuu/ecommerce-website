from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist
from .serializers import WishlistSerializer
from apps.products.models import Product

class WishlistListView(generics.ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).order_by('-created_at')

class WishlistAddView(generics.CreateAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )

        serializer = self.get_serializer(wishlist_item)
        if created:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_200_OK)

class WishlistRemoveView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        try:
            item = Wishlist.objects.get(user=request.user, product_id=product_id)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Wishlist.DoesNotExist:
            return Response({'error': 'Item not in wishlist'}, status=status.HTTP_404_NOT_FOUND)
