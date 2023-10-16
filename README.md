# Proyecto grupal de Coding Dojo "Cervantes representaciones"
## Versiones:
### Version 1.0 (Proyecto Individual: Diego Caceres):
- Creacion de modelos: Book, Order, Category.
- Creacion de templates para Inicio, Sobre Nosotros, Libros, Carrito, etc.
- Despliegue de libros por categorias en el template books.
- Implementacion de boton para ver todos los libros dentro de una categoria.
- Implementacion de boton para ver detalles del libro en un modal, utilizando Json para los datos.
- Implementacion de boton para ordenar el pedido que renderiza un formulario.
- Formulario con datos del cliente y del libro seleccionado, el pedido ser guarda en el modelo Order.

### Version 2.0 (Proyecto Grupal: Diego Caceres y Fredy Arce):
- Reestructuracion de carpetas segun el Modelo-Vista-Controlador.
- Implementacion de Login y Register con autenticacion.
- Implementacion de buscador de libros por titulo.
- Implementacion de paginador para los libros.
- Optimizacion del carrito de compras:
  - Implementacion de guardado de libros en sesion.
  - Implementacion de subtotal y total.
- Creacion del modelo Order Details.
- Personalizacion de admin de Django para poder ver libros y ordenes.

## Descripción del proyecto 
- **Registro e Inicio de Sesión de Usuarios:** Los usuarios pueden registrarse en el sistema e iniciar sesión en la aplicación.
- **Búsqueda de Libros:** Los usuarios tienen a su disposición una interfaz para buscar los libros de sus preferencias.
- **Detalles del libro:** Una vez que los usuarios hayan filtrado un libro de su interés, pueden ver información detallada, incluyendo imágenes, descripción y precio.
- **Agregar al carrito** Los usarios podran agreagar al carrito los libros de sus intereses.
## Instalación de la Aplicación Web 

### Pasos para configurar el entorno virtual, instalar Django y las dependencias desde el archivo `requirements.txt`:
```bash
pip install -r requeriments.txt
```
