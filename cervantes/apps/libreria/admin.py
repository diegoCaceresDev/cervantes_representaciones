from django.contrib import admin
from .models import Category, Book, Order
from django.utils.html import format_html

# Register your models here.
admin.site.register(Category)
admin.site.register(Order)


@admin.register(Book)
class BooAdmin(admin.ModelAdmin):
    list_display = ('isbn', 'category', 'price', 'stock', 'display_image')
    list_filter = ('category', 'price')
    search_fields = ('title', 'category__name')
    list_per_page = 6

    def display_image(self, obj):
        if obj.img:
            return format_html('<img src="{}" width="50" height="50" />', obj.img.url)
        else:
            return 'No Image Found'

    display_image.short_description = 'Image'


