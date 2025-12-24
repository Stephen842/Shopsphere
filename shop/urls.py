from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductViewSet, CartViewSet, OrderViewSet

router = DefaultRouter()

# Public endpoints
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

# Authenticated endpoints
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = router.urls