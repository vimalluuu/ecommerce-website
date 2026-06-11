import uuid
from django.utils import timezone
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, Coupon
from .serializers import OrderSerializer
from django.http import HttpResponse
from reportlab.pdfgen import canvas

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(order_number=str(uuid.uuid4().hex)[:10].upper())

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class CouponValidateView(views.APIView):
    def post(self, request):
        code = request.data.get('code')
        order_amount = request.data.get('order_amount', 0)
        
        try:
            coupon = Coupon.objects.get(code__iexact=code, is_active=True)
            if coupon.expires_at and coupon.expires_at < timezone.now():
                return Response({'error': 'Coupon expired'}, status=status.HTTP_400_BAD_REQUEST)
            if coupon.max_uses and coupon.uses_count >= coupon.max_uses:
                return Response({'error': 'Coupon usage limit reached'}, status=status.HTTP_400_BAD_REQUEST)
            if float(order_amount) < coupon.min_order_amount:
                return Response({'error': f'Minimum order amount must be {coupon.min_order_amount}'}, status=status.HTTP_400_BAD_REQUEST)
            
            discount = 0
            if coupon.discount_type == 'percentage':
                discount = (float(order_amount) * float(coupon.discount_value)) / 100
            else:
                discount = float(coupon.discount_value)
                
            return Response({
                'valid': True,
                'discount_amount': discount,
                'coupon_id': coupon.id
            })
        except Coupon.DoesNotExist:
            return Response({'error': 'Invalid coupon code'}, status=status.HTTP_404_NOT_FOUND)

class ShippingCostView(views.APIView):
    def post(self, request):
        # Dummy logic: Free shipping over 2999, else 150
        order_amount = float(request.data.get('order_amount', 0))
        cost = 0 if order_amount >= 2999 else 150
        return Response({'shipping_cost': cost})

class OrderInvoiceView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.get(id=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
            
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{order.order_number}.pdf"'
        
        p = canvas.Canvas(response)
        p.drawString(100, 800, f"Invoice for Order: {order.order_number}")
        p.drawString(100, 780, f"Date: {order.created_at.strftime('%Y-%m-%d')}")
        p.drawString(100, 760, f"Total Amount: Rs. {order.total_amount}")
        p.drawString(100, 740, f"Payment Status: {order.payment_status}")
        p.showPage()
        p.save()
        return response
