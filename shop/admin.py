from django.contrib import admin

from .models import Category, Product, Subcategory, CartItem

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(CartItem)