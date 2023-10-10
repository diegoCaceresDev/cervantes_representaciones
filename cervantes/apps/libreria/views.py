from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Category
from django.http import JsonResponse
from django.contrib import messages
from .forms import book_form
from .models import Order
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# Renderiza el `inicio`
def index(request):
    return render(request, "dashboard/index.html")


# Renderiza el `sobre nosotros`
def about_us(request):
    return render(request, "dashboard/about.html")


# Renderiza el `libros`
def books(request):
    context = {
        "categories": Category.objects.all(),
    }

    return render(request, "dashboard/books.html", context)


# Renderiza  `libros` filtrado por especialidad
def books_speciality(request, category_id):
    category = Category.objects.get(id=category_id)
    book = category.books.all()
    paginator = Paginator(book, 3)
    page = request.GET.get('page')
    books_page = paginator.get_page(page)
    context = {
        "category": category,
        "books_page": books_page
    }
    return render(request, "dashboard/books_speciality.html", context)


# Renderiza el `cart`
def cart(request):
    return render(request, "dashboard/cart_with_book.html")


# Obtener detalles del libro en Json

def book_detail(request, book_id):
    try:
        book = get_object_or_404(Book, pk=book_id)
        detalles = {
            "title": book.title,
            "description": book.description,
            "publication_date": str(book.publication_date),
            "author": book.author,
            "price": str(book.price),
            "category": str(book.category),
        }
        return JsonResponse(detalles)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'El libro no existe'}, status=404)


# Renderiza el `cart with book`
def cart_with_book(request, book_id):

    # Recupera la variable de sesión 'cart' o crea un diccionario vacío si no existe
    cart = request.session.get('cart', {})

    # Agrega el libro al carrito utilizando su ID como clave y la cantidad deseada como valor
    cart[book_id] = cart.get(book_id, 0) + 1

    # Almacena el carrito actualizado en la variable de sesión
    request.session['cart'] = cart

    books = []
    for book in request.session['cart'].keys():
        books.append(Book.objects.filter(id=book))

    print(f"Esto: {books}")
    context = {
        "books": books,
    }

    return render(request, "dashboard/cart_with_book.html", context)



# Renderiza el `form`
@login_required
def form(request, book_id):
    book_by_id = Book.objects.filter(id=book_id)
    context = {
        "book": book_by_id,
    }
    return render(request, "dashboard/form.html", context)


# Formulario de compra
def process_book(request):
    if request.method == "POST":
        form = book_form(request.POST)
        if form.is_valid():
            new_order = Order(
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                phone=form.cleaned_data["phone"],
                title=form.cleaned_data["title"],
                price=form.cleaned_data["price"],
            )
            new_order.save()
            messages.success(request, 'Tu pedido ha sido procesado')
            return redirect("/books")
        else:
            messages.error(request, 'Algo ha salido mal')
            return render(request, 'dashboard/index.html')


def search_book(request):
    if request.method == "POST":
        # Obtenemos la entrada del usuario
        search_query = request.POST['search_query']
        # Fitramos la entrada para obtener las coincidencias
        books = Book.objects.filter(title__icontains=search_query)
        # Contamos la cantidad de resultados obtenidos
        count_result = books.count()
        print(count_result)
        print(books)
        context = {
            'query': search_query,
            'books': books,
            'cantidad': count_result
        }
        return render(request, 'dashboard/books.html', context)
