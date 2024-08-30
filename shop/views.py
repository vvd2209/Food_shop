from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Category, Subcategory, Product, CartItem
from .serializers import CategorySerializer, SubcategorySerializer, ProductSerializer, CartItemSerializer, \
    CartSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ Представление категорий """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ Представление подкатегорий """

    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """ Представление продуктов """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartViewSet(viewsets.ModelViewSet):
    """ Представление корзины """

    serializer_class = CartItemSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """ Возвращает queryset товаров в корзине текущего пользователя """

        return CartItem.objects.filter(user=self.request.user.id)

    def create(self, request):
        """ Создает новый товар в корзине или обновляет его количество """

        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Товар не найден'},
                            status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """ Обновляет количество товара в корзине """

        try:
            cart_item = CartItem.objects.get(id=pk, user=request.user)
        except CartItem.DoesNotExist:
            return Response({'error': 'Корзина пустая'},
                            status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get('quantity')
        if quantity:
            cart_item.quantity = int(quantity)
            cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def view_cart(self, request):
        """ Возвращает содержимое корзины с указанием количества товаров и суммы """

        cart_items = self.get_queryset()
        total_items = sum(
            item.quantity for item in cart_items
        )
        total_price = sum(
            item.product.price * item.quantity for item in cart_items
        )

        serializer = CartSerializer({
            'items': cart_items,
            'total_items': total_items,
            'total_price': total_price
        })
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def clear_cart(self, request):
        """ Очищает корзину пользователя """

        self.get_queryset().delete()
        return Response({'message': 'Корзина очищена'}, status=status.HTTP_200_OK)
