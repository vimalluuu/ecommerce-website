from rest_framework import serializers
from .models import Order, OrderItem, Coupon

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_image', 'quantity', 'size', 'color', 'price']

    def get_product_image(self, obj):
        if obj.product and obj.product.image_urls:
            return obj.product.image_urls[0] if len(obj.product.image_urls) > 0 else None
        return None

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    write_items = serializers.ListField(child=serializers.DictField(), write_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'total_amount', 'discount_amount', 'shipping_cost',
            'payment_status', 'order_status', 'shipping_address', 'coupon', 'tracking_number',
            'notes', 'created_at', 'items', 'write_items'
        ]
        read_only_fields = ['user', 'payment_status', 'order_status', 'order_number']

    def create(self, validated_data):
        items_data = validated_data.pop('write_items', [])
        user = self.context['request'].user
        if user.is_authenticated:
            validated_data['user'] = user
        order = Order.objects.create(**validated_data)
        
        for item in items_data:
            OrderItem.objects.create(
                order=order,
                product_id=item.get('product_id'),
                quantity=item.get('quantity'),
                size=item.get('size'),
                color=item.get('color'),
                price=item.get('price')
            )
        return order

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'
