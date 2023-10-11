from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Category
from django.http import JsonResponse
from django.contrib import messages
from .forms import book_form
from .models import Order, OrderDetail
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


# Renderiza el `cart`, todos los pedidos de libros que hay en la session y calcula el precio total.
def cart(request):
    """
    Devuelve el carrito con los books solicitados por el usuario en sesion, la cantidad y 
    el precio sub-total de cada pedido y precio total de todos los pedidos.
    """
    books = []
    quantity = []
    subtotal = []
    total = 0
    cart = request.session.get('cart', {})

    if not cart:
        request.session['cart'] = {}
    # Guarda todos los books solicitados por el usuario en sesion en la variable books
    for book in cart.keys():
        books.append(Book.objects.filter(id=book))

    # Guarda todos cantidad de cada book solicitados por el usuario en sesion en la variable quantity
    for book in cart.items():
        quantity.append(book)

    print(f"esto es la cantidad: {quantity}")

    # Guarda el precio subtotal de cada pedido en la variable subtotal
    for book_quantity in quantity:
        for object in books:
            for book in object:
                if book.id == int(book_quantity[0]):
                    subtotal_book = book.price * book_quantity[1]
                    subtotal.append((book.id, subtotal_book))
    print(f"esto es el subtotal: {subtotal}")

    # Guarda el precio total de todos los pedidos en la variable total
    for precio in subtotal:
        total += precio[1]
    print(f"esto es el total: {total}")

    context = {
        "books": books,
        "total": total,
        "subtotal": subtotal,
        "quantity": quantity,
    }
    return render(request, "dashboard/cart.html", context)


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
    cart[str(book_id)] = cart.get(str(book_id), 0) + 1

    # Almacena el carrito actualizado en la variable de sesión
    request.session['cart'] = cart

    books = []
    for book in request.session['cart'].keys():
        books.append(Book.objects.filter(id=book))

    print(f"Esto: {books}")
    context = {
        "books": books,
    }
    messages.success(request, 'Se ha añadido el libro a su carrito de compra')

    return render(request, "dashboard/cart_with_book.html", context)


def create_order(request):
    # Obtener el carrito de la sesión
    cart = request.session.get('cart', {})

    # Crea una instancia de Order y asocia al usuario
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    order = Order(user=user, total=0)

    # Guarda el pedido
    order.save()

    # Creando detalles de la orden
    for book_id, stock in cart.items():
        book = Book.objects.get(id=book_id)
        subtotal = book.price * stock  # Calcula el subtotal para este libro

        order_detail = OrderDetail(order=order, book=book, quantity=stock, subtotal=subtotal)
        order_detail.save()

    # Calculando el monmto total del orden
    order.calculate_total()
    order.save()

    # Limpia el carrito en la sesión
    request.session['cart'] = {}

    messages.success(request, 'La orden se ha creado con éxito')
    return render(request, 'dashboard/index.html')


# Renderiza el `form`
@login_required
def form(request):
    books = []
    total = 0
    cart = request.session.get('cart', {})

    for book in cart.keys():
        books.append(Book.objects.filter(id=book))

    for object in books:
        for book in object:
            total += book.price

    context = {
        "books": books,
        "total": total,
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
