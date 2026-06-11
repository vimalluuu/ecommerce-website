"""
Products app models — Category, Product, Review.
"""

import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Product category."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True, default='')
    image_url = models.URLField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Product(models.Model):
    """A product in the ARCFORM catalog."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=320, unique=True, blank=True)
    description = models.TextField(blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    compare_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0)],
        help_text="Original price before discount (for strikethrough display)",
    )
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
    )
    # JSONField lists
    image_urls = models.JSONField(
        default=list,
        help_text="List of image URL strings",
    )
    sizes = models.JSONField(
        default=list,
        help_text="List of available size strings e.g. ['XS','S','M','L','XL']",
    )
    colors = models.JSONField(
        default=list,
        help_text="List of available color strings e.g. ['Black','White']",
    )
    tags = models.JSONField(
        default=list,
        help_text="List of tag strings e.g. ['streetwear','hoodie','limited']",
    )
    is_featured = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0.0
        return round(sum(r.rating for r in reviews) / len(reviews), 1)

    @property
    def review_count(self):
        return self.reviews.count()

    @property
    def discount_percentage(self):
        if self.compare_price and self.compare_price > self.price:
            return round(((self.compare_price - self.price) / self.compare_price) * 100)
        return 0


class Review(models.Model):
    """Customer review on a product."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    review_text = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reviews'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.name} — {self.product.name} ({self.rating}★)"
