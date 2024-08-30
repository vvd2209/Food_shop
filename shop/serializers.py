from rest_framework import serializers
from .models import Category, Subcategory, Product, CartItem


class CategorySerializer(serializers.ModelSerializer):
    """ Сериализатор для категорий """

    subcategories = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'subcategories']


class SubcategorySerializer(serializers.ModelSerializer):
    """ Сериализатор для подкатегорий """

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'slug', 'category', 'image']


class ProductSerializer(serializers.ModelSerializer):
    """ Сериализатор для продуктов """

    category = serializers.SerializerMethodField()
    subcategory = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category', 'subcategory', 'price', 'images']

    def get_category(self, obj):
        """Возвращает название категории продукта."""

        return obj.subcategory.category.name

    def get_subcategory(self, obj):
        """Возвращает название подкатегории продукта."""

        return obj.subcategory.name

    def get_images(self, obj):
        """Возвращает словарь с URL изображений продукта разных размеров."""

        return {
            'small': obj.image_small.url,
            'medium': obj.image_medium.url,
            'big': obj.image_big.url,
        }


class CartItemSerializer(serializers.ModelSerializer):
    """Сериализатор для модели товара в корзине."""

    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class CartSerializer(serializers.Serializer):
    """Сериализатор для представления корзины."""

    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
