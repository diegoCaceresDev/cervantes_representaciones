from typing import Any
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
        
    def __str__(self):
        return f"{self.name}"
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        
    
class Order(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    date = models.DateField(auto_now_add=True)
    phone = models.IntegerField(null=True)
    title = models.CharField(max_length=100, null=True)
    price = models.IntegerField(null=True)
    
    
    def __str__(self):
        return f"Pedido de {self.first_name} {self.last_name}. Fecha del pedido: {self.date}"
    
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"


class Book(models.Model):
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    publication_date = models.DateField(null=True)
    author = models.CharField(max_length=100, null=True)
    price = models.IntegerField(null=True)
    img = models.ImageField(upload_to="book/", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, related_name=("books"), null=True, on_delete=models.CASCADE)        

    def __str__(self):
        return f"{self.title} by: {self.author}"
    
    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"



