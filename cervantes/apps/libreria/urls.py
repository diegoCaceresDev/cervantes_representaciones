from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from apps.libreria import views

app_name = "bookstore"

urlpatterns = [
    path('', views.index, name='index'),
    path('about_us', views.about_us),
    path('books', views.books),
    path('cart', views.cart),
    path('cart/<int:book_id>/', views.cart_with_book, name='cart_with_book'),
    path('book_detail/<int:book_id>/', views.book_detail, name='book_detail'),
    path('books_speciality/<int:category_id>/', views.books_speciality, name='books_speciality'),
    path('form', views.form, name='form'),
    path('process_book', views.process_book, name='process_book'),
    path('search/', views.search_book, name='search'),
    path('create_order', views.create_order, name='create_order')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
