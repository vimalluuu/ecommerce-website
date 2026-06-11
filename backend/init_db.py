import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arcform.settings')
django.setup()

from apps.users.models import User
from apps.products.models import Category, Product
from apps.orders.models import Order, OrderItem
import datetime

def populate():
    print("Creating test user...")
    user, _ = User.objects.get_or_create(email='test@example.com')
    if not user.has_usable_password():
        user.set_password('password123')
        user.name = 'Test User'
        user.is_email_verified = True
        user.save()

    print("Creating categories...")
    categories = [
        {'name': 'Outerwear', 'description': 'Jackets and coats.', 'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&q=80&w=600'},
        {'name': 'Essentials', 'description': 'Everyday wear.', 'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&q=80&w=600'},
        {'name': 'Accessories', 'description': 'Hats, bags, etc.', 'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&q=80&w=600'},
    ]
    created_categories = {}
    for cat_data in categories:
        cat, created = Category.objects.get_or_create(name=cat_data['name'], defaults=cat_data)
        if not created:
            cat.image_url = cat_data['image_url']
            cat.save()
        created_categories[cat.name] = cat

    print("Creating products...")
    products = [
        {
            'name': 'Void Nylon Bomber',
            'description': 'A premium structured nylon bomber jacket perfect for layering. Water-resistant and insulated.',
            'price': 340.00,
            'stock': 42,
            'category': created_categories['Outerwear'],
            'sizes': ['S', 'M', 'L', 'XL'],
            'colors': ['Black', 'Olive'],
            'image_urls': ['https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&q=80&w=800'],
            'is_featured': True,
        },
        {
            'name': 'Heavyweight Hoodie',
            'description': 'Ultra-premium heavyweight cotton hoodie with a dropped shoulder fit and double-lined hood.',
            'price': 180.00,
            'stock': 12,
            'category': created_categories['Essentials'],
            'sizes': ['S', 'M', 'L', 'XL'],
            'colors': ['Black', 'Concrete Grey', 'Washed Brown'],
            'image_urls': ['https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&q=80&w=800'],
            'is_featured': True,
        },
        {
            'name': 'Structured Trench Coat',
            'description': 'Modern minimalist trench coat made with breathable technical fabric.',
            'price': 420.00,
            'stock': 5,
            'category': created_categories['Outerwear'],
            'sizes': ['M', 'L'],
            'colors': ['Sand', 'Black'],
            'image_urls': ['https://images.unsplash.com/photo-1539533113208-f6df8cc8b543?auto=format&fit=crop&q=80&w=800'],
            'is_featured': False,
        },
        {
            'name': 'Tactical Cargo Pants',
            'description': 'Durable cargo pants with articulated knees and multiple hidden zip pockets.',
            'price': 220.00,
            'stock': 30,
            'category': created_categories['Essentials'],
            'sizes': ['28', '30', '32', '34', '36'],
            'colors': ['Black', 'Navy'],
            'image_urls': ['https://images.unsplash.com/photo-1517438476312-10d79c077509?auto=format&fit=crop&q=80&w=800'],
            'is_featured': True,
        },
        {
            'name': 'Minimalist Tote',
            'description': 'A daily carry tote bag made of heavy canvas with leather reinforced straps.',
            'price': 110.00,
            'stock': 100,
            'category': created_categories['Accessories'],
            'sizes': ['OS'],
            'colors': ['Off-White', 'Black'],
            'image_urls': ['https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&q=80&w=800'],
            'is_featured': False,
        }
    ]

    for p_data in products:
        product, created = Product.objects.get_or_create(name=p_data['name'], defaults=p_data)
        if not created:
            for k, v in p_data.items():
                setattr(product, k, v)
            product.save()

    print("Creating demo orders...")
    # Clean old orders for test user
    Order.objects.filter(user=user).delete()
    
    order1 = Order.objects.create(
        user=user,
        order_number='ORD-092',
        total_amount=355.00,
        shipping_cost=15.00,
        payment_status='paid',
        order_status='processing',
        shipping_address={"name": "Test User", "address": "123 Main St", "city": "Mumbai", "postal": "400001"}
    )
    product1 = Product.objects.get(name='Void Nylon Bomber')
    OrderItem.objects.create(order=order1, product=product1, quantity=1, price=340.00, size='M', color='Black')

    order2 = Order.objects.create(
        user=user,
        order_number='ORD-085',
        total_amount=195.00,
        shipping_cost=15.00,
        payment_status='paid',
        order_status='delivered',
        shipping_address={"name": "Test User", "address": "123 Main St", "city": "Mumbai", "postal": "400001"}
    )
    product2 = Product.objects.get(name='Heavyweight Hoodie')
    OrderItem.objects.create(order=order2, product=product2, quantity=1, price=180.00, size='L', color='Concrete Grey')

    print("Database population complete!")

if __name__ == '__main__':
    populate()
