from django.contrib import admin
from .models import Category, Book, Order

# Register your models here.
admin.site.register(Category)
admin.site.register(Order)


@admin.register(Book)
class BooAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'img')


