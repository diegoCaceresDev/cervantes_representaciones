from typing import Any
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField('nombre', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


class Book(models.Model):
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    publication_date = models.DateField(null=True)
    author = models.CharField(max_length=100, null=True)
    editorial = models.CharField(max_length=100, null=True)
    price = models.IntegerField('Precio', null=True)
    isbn = models.CharField(max_length=13, unique=True, default='Sin ISBN')
    stock = models.IntegerField('Cantidad', null=True)
    img = models.ImageField('Portada', upload_to="book/", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, related_name=("books"), null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} by: {self.author}"

    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"


# Necesito una clase order y una clase order detail para libto
class Order(models.Model):
    user = models.ForeignKey(User, related_name=("orders"), null=True, on_delete=models.CASCADE)
    total = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total(self):
        order_details = self.order_details.all()
        total = sum(detail.subtotal for detail in order_details)
        self.total = total
        self.save()

    def __str__(self):
        return f"{self.user} - {self.total}"

    class Meta:
        verbose_name = "Orden"
        verbose_name_plural = "Ordenes"


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name=("order_details"), null=True, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name=("order_details"), null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    subtotal = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order} - {self.book}"

    class Meta:
        verbose_name = "Detalle de Orden"
        verbose_name_plural = "Detalles de Ordenes"
