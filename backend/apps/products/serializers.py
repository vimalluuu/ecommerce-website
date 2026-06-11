from rest_framework import serializers
from .models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_avatar = serializers.CharField(source='user.avatar_url', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_name', 'user_avatar', 'product', 'rating', 'review', 'created_at']
        read_only_fields = ['user', 'product']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'compare_price', 'stock',
            'category', 'category_id', 'image_urls', 'sizes', 'colors', 'tags',
            'is_featured', 'is_active', 'created_at', 'reviews', 'average_rating', 'review_count'
        ]

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(r.rating for r in reviews) / len(reviews)
        return 0

    def get_review_count(self, obj):
        return obj.reviews.count()
