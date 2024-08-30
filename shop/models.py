from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    """ Модель представления класса Категория """

    name = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True, verbose_name='slug-имя')
    image = models.ImageField(upload_to='categories/', verbose_name='Изображение')

    def save(self, *args, **kwargs):
        """ Автоматическое создание slug-имени """
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Subcategory(models.Model):
    """ Модель представления класса Подкатегория """

    name = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True, verbose_name='slug-имя')
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE,
                                 verbose_name='Категория')
    image = models.ImageField(upload_to='subcategories/', verbose_name='Изображение')

    def save(self, *args, **kwargs):
        """ Автоматическое создание slug-имени """
        if not self.slug:
            self.slug = slugify(self.name)
        super(Subcategory, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ('name',)


class Product(models.Model):
    """ Модель представления класса Продукт """

    name = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True, verbose_name='slug-имя')
    subcategory = models.ForeignKey(Subcategory, related_name='products', on_delete=models.CASCADE,
                                    verbose_name='Подкатегория')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE,
                                 verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')
    image_small = models.ImageField(upload_to='products/small/', verbose_name='Изображение-small')
    image_medium = models.ImageField(upload_to='products/medium/', verbose_name='Изображение-medium')
    image_big = models.ImageField(upload_to='products/big/', verbose_name='Изображение-big')

    def save(self, *args, **kwargs):
        """ Автоматическое создание slug-имени """
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('name',)


class CartItem(models.Model):
    """ Модель представления класса Корзина """

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Состав корзины'
        verbose_name_plural = 'Состав корзины'
