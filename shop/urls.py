from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, SubcategoryViewSet, ProductViewSet, CartViewSet

app_name = 'shop'

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('subcategories', SubcategoryViewSet, basename='subcategories')
router.register('products', ProductViewSet, basename='products')
router.register('cart', CartViewSet, basename='cart')

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include('djoser.urls')),
    path("auth/", include('djoser.urls.authtoken')),
    # Создание нового пользователя shop/auth/users/
    # Авторизация пользователя     shop/auth/token/login/
]