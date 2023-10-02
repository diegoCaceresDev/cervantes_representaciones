# Django
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

# Forms
from apps.users.forms import CustomUserCreationForm


def register(request):
    """
    Vista para el registro de usuarios.

    Esta vista permite a los usuarios registrarse en el sistema. Se manejan dos métodos HTTP: GET y POST.

    Para el método GET:
    - Muestra el formulario de registro en la página 'user/register.html'.

    Para el método POST:
    - Valida el formulario de registro enviado por el usuario.
    - Si el formulario es válido, crea una nueva cuenta de usuario y redirige al usuario a la página de inicio de sesión.
    - Si el formulario no es válido, muestra los errores en la misma página de registro.

    :param request: La solicitud HTTP enviada por el cliente.
    :type request: HttpRequest

    :return: Si el método es POST y el formulario es válido, redirecciona a 'user:login'.
             Si el método es POST y el formulario no es válido, muestra los errores en 'user/register.html'.
             Si el método es GET, muestra el formulario de registro en 'user
             /register.html'.
    :rtype: HttpResponse
    """

    if request.method == 'POST':  # noqa: E501
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():  # Aca validamos
            user = form.save()  # aca guardamos
            messages.success(request, 'Usuario creado correctamente, puedes iniciar sesión.')
            # profile = Profile(user=user) # creamos un perfil
            # profile.save() # guardamos usario en sesion
            return redirect('user:login')
        else:
            errors = form.errors
            return render(request, 'user/register.html', {'errors': errors})
    else:
        return render(request, 'user/register.html')


def user_login(request):
    """
    Vista para la autenticación de usuarios.

    Esta vista permite a los usuarios iniciar sesión en el sistema. Maneja dos métodos HTTP: GET y POST.

    Para el método GET:
    - Muestra el formulario de inicio de sesión en la página 'user/login.html'.

    Para el método POST: - Verifica las credenciales del usuario proporcionadas en el formulario de inicio de sesión.
    - Si las credenciales son correctas, inicia sesión en la cuenta del usuario y redirige a 'hotel:index'. - Si las
    credenciales son incorrectas, muestra un mensaje de error en la página y vuelve a mostrar el formulario de inicio
    de sesión.

    :param request: La solicitud HTTP enviada por el cliente.
    :type request: HttpRequest

    :return: Si el método es POST y las credenciales son correctas, redirecciona a 'hotel:index'. Si el método es
    POST y las credenciales son incorrectas, muestra un mensaje de error y vuelve a mostrar el formulario. Si el
    método es GET, muestra el formulario de inicio de sesión en 'user/login.html'. :rtype: HttpResponse
    """  # noqa: E501
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Has iniciado sesión correctamente.')
            # if not user.profile.profile:
            # return redirect('user:updated', user_id=user.id, username=user.username)
            # else:
            #   return redirect('user:profile', user_id=user.id, username=user.username)
            return redirect('bookstore:index')
        else:
            messages.error(request, 'Las credenciales proporcionadas son incorrectas. '
                                    'Por favor, inténtalo de nuevo.')
    return render(request, 'user/login.html')


def user_logout(request):
    """
    Cerrar sesión de un usuario.

    Esta vista permite a un usuario cerrar sesión en su cuenta.

    Args:
        request (HttpRequest): La solicitud HTTP que activa la vista.

    Returns:
        HttpResponseRedirect: Redirige al usuario a la página de inicio de sesión.
    """
    logout(request)
    messages.warning(request, 'Has cerrado sesión.')
    return redirect('user:login')


