from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
import uuid


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(default=0)  # stock quantity
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    def reduce_stock(self, quantity):
        """Reduce stock by quantity. Raises ValueError if insufficient."""
        if quantity > self.stock:
            raise ValueError("Insufficient stock for product: %s" % self.pk)
        self.stock = models.F('stock') - quantity
        self.save(update_fields=['stock'])


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='cart', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart({self.user})"

    def total(self):
        """Return cart total as Decimal."""
        total = sum(item.subtotal() for item in self.items.select_related('product'))
        return total

    def clear(self):
        """Remove all items from cart."""
        self.items.all().delete()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def subtotal(self):
        return self.product.price * self.quantity


class Order(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    # Use UUID for public-facing id if you like; keep numeric pk for DB
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    placed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.uuid} by {self.user}"

    @classmethod
    def create_from_cart(cls, cart):
        """
        Create an Order from a Cart instance.
        This will copy CartItems into OrderItems and optionally reduce product stock.
        """
        if not cart.items.exists():
            raise ValueError("Cart is empty")

        total = sum(item.subtotal() for item in cart.items.select_related('product'))

        order = cls.objects.create(user=cart.user, total_amount=total, placed_at=timezone.now())

        order_items = []
        for item in cart.items.select_related('product'):
            # Save price at purchase time
            oi = OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            order_items.append(oi)
            # reduce stock - consider wrapping in transaction in real impl
            if item.product.stock < item.quantity:
                # rollback behaviour should be implemented at view or service layer
                raise ValueError(f"Insufficient stock for product {item.product.pk}")
            item.product.stock = models.F('stock') - item.quantity
            item.product.save(update_fields=['stock'])

        OrderItem.objects.bulk_create(order_items)
        # clear the cart
        cart.clear()
        return order


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)  # price at time of purchase

    def __str__(self):
        return f"{self.quantity} x {self.product.name} @ {self.price}"
