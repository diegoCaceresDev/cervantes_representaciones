from django.contrib import admin
from .models import Category, Book, Order, OrderDetail
from django.utils.html import format_html

# Register your models here.
admin.site.register(Category)


@admin.register(Book)
class BooAdmin(admin.ModelAdmin):
    list_display = ('isbn', 'category', 'editorial', 'price', 'stock', 'display_image')
    list_filter = ('category', 'price')
    search_fields = ('title', 'category__name')
    list_per_page = 6

    def display_image(self, obj):
        if obj.img:
            return format_html('<img src="{}" width="50" height="50" />', obj.img.url)
        else:
            return 'No Image Found'

    display_image.short_description = 'Portada'


class OrderDetailInline(admin.TabularInline):  # Puedes cambiar a StackedInline si prefieres una vista apilada
    model = OrderDetail
    extra = 1  # Puedes ajustar esto para especificar cuántos detalles de órdenes puedes agregar


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total', 'created_at', 'updated_at')
    list_filter = ('user',)
    inlines = [OrderDetailInline]  # Agrega el Inline de detalles de órdenes a la vista de órdenes
