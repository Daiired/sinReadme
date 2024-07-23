from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Alimento, CategoriaAlimento, Dieta, LibreDeAlimento, AlimentoLibreDe, AlimentoDieta, Carrito, CarritoItem, Pedido, PedidoItem
from .forms import ContactoForm, ProductoForm, CustomUserCreationForm, AlimentoForm, CategoriaForm, DietaForm, LibreForm, AlimentoDietaForm, AlimentoLibreDeForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.conf import settings
import paypalrestsdk
from .paypal_config import *
from paypalrestsdk import Payment
# Create your views here.


def index(request):
    return render(request, 'app/index.html')



from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def home(request):
    categorias = CategoriaAlimento.objects.all()
    dietas = Dieta.objects.all()
    libres_alimentos = LibreDeAlimento.objects.all()

    productos = Alimento.objects.all()

    categoria_seleccionada = request.GET.get('categoria')
    dietas_seleccionadas = request.GET.getlist('dieta')
    alimentos_libres_seleccionados = request.GET.getlist('libre_alimento')
    busqueda = request.GET.get('search')

    if busqueda:
        productos = productos.filter(nombre_alimento__icontains=busqueda)
    if categoria_seleccionada:
        productos = productos.filter(id_categoria=categoria_seleccionada)

    if dietas_seleccionadas:
        productos = productos.filter(alimentodieta__id_dieta__in=dietas_seleccionadas).distinct()
        for dieta_id in dietas_seleccionadas:
            productos = productos.filter(alimentodieta__id_dieta=dieta_id).distinct()

    if alimentos_libres_seleccionados:
        productos = productos.filter(alimentolibrede__id_libre__in=alimentos_libres_seleccionados).distinct()
        for libre_id in alimentos_libres_seleccionados:
            productos = productos.filter(alimentolibrede__id_libre=libre_id).distinct()

    # Paginación
    page = request.GET.get('page', 1)
    paginator = Paginator(productos, 5)  # Mostrar 5 productos por página

    try:
        productos_paginados = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un entero, mostrar la primera página.
        productos_paginados = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango (por ejemplo, 9999), mostrar la última página de resultados.
        productos_paginados = paginator.page(paginator.num_pages)

    data = {
        'productos': productos_paginados,
        'categorias': categorias,
        'dietas': dietas,
        'libres_alimentos': libres_alimentos,
        'categoria_seleccionada': categoria_seleccionada,
        'dietas_seleccionadas': dietas_seleccionadas,
        'alimentos_libres_seleccionados': alimentos_libres_seleccionados,
        'paginator': paginator
    }
    return render(request, 'app/home.html', data)

@login_required
def contacto(request):
    data = {
        'form': ContactoForm()
    }

    if request.method == 'POST':
        formulario = ContactoForm(data= request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Contacto enviado")
        else:
            data["form"] = formulario

    return render(request, 'app/contacto.html', data )

@login_required
def galeria(request):
    return render(request, 'app/galeria.html')

def descripcion_producto(request, id):
    alimento = get_object_or_404(Alimento, id=id)
    dietas_compatibles = AlimentoDieta.objects.filter(alimento=alimento).values_list('id_dieta__nombre', flat=True)
    restricciones_alimentarias = AlimentoLibreDe.objects.filter(alimento=alimento).values_list('id_libre__nombre', flat=True)
    return render(request, 'app/detalle.html', {'alimento': alimento, 'dietas_compatibles': dietas_compatibles, 'restricciones_alimentarias': restricciones_alimentarias})

#Alimentos CRUD

@permission_required('app.add_alimento')
def agregar_Alimento(request):
    
    data ={
        'form': AlimentoForm()
    }
    
    if request.method == 'POST':
        formulario = AlimentoForm(data=request.POST, files =request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Alimento registrado")
        else:
            data["form"] = formulario 

    return render(request, 'app/alimento/agregar.html',data)

@permission_required('app.view_alimento')
def listar_Alimentos(request):
    alimentos = Alimento.objects.all()
    page = request.GET.get('page',1)

    try:
        paginator = Paginator(alimentos, 5)
        alimentos = paginator.page(page)
    except:
        raise Http404
    

    data ={
        'entity': alimentos,
        'paginator': paginator
    }
    return render(request, 'app/alimento/listar.html', data)

@permission_required('app.change_alimento')
def modificar_Alimento(request, id):
    alimento = get_object_or_404(Alimento, id=id)
    
    data ={
        'form': AlimentoForm(instance=alimento)
    }

    if request.method == 'POST':
        formulario = AlimentoForm(data= request.POST, instance=alimento, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect(to="listar_alimentos")
        data["form"] =formulario


    return render(request, 'app/alimento/modificar.html',data )

@permission_required('app.delete_alimento')
def eliminar_Alimento(request, id):
    alimento= get_object_or_404(Alimento, id=id)
    alimento.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect(to="listar_alimentos")

#CategoriaAlimentos CRUD

@permission_required('app.add_categoria_alimento')
def agregar_Categoria(request):
    
    data ={
        'form': CategoriaForm()
    }
    
    if request.method == 'POST':
        formulario = CategoriaForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Categoria registrada")
        else:
            data["form"] = formulario 

    return render(request, 'app/categoria/agregar.html',data)

@permission_required('app.view_categoria_alimento')
def listar_Categorias(request):
    categorias = CategoriaAlimento.objects.all()
    page = request.GET.get('page',1)

    try:
        paginator = Paginator(categorias, 5)
        categorias = paginator.page(page)
    except:
        raise Http404
    

    data ={
        'entity': categorias,
        'paginator': paginator
    }
    return render(request, 'app/categoria/listar.html', data)

@permission_required('app.change_categoria_alimento')
def modificar_Categoria(request, id):
    categoria = get_object_or_404(CategoriaAlimento, id=id)
    
    data ={
        'form': CategoriaForm(instance=categoria)
    }

    if request.method == 'POST':
        formulario = CategoriaForm(data= request.POST, instance=categoria)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect(to="listar_categorias")
        data["form"] =formulario


    return render(request, 'app/categoria/modificar.html',data )

@permission_required('app.delete_categoria_alimento')
def eliminar_Categoria(request, id):
    categoria= get_object_or_404(CategoriaAlimento, id=id)
    categoria.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect(to="listar_categorias")

#Dieta CRUD

@permission_required('app.add_dieta')
def agregar_Dieta(request):
    
    data ={
        'form': DietaForm()
    }
    
    if request.method == 'POST':
        formulario = DietaForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Dieta registrada")
        else:
            data["form"] = formulario 

    return render(request, 'app/dieta/agregar.html',data)

@permission_required('app.view_dieta')
def listar_Dietas(request):
    dietas = Dieta.objects.all()
    page = request.GET.get('page',1)

    try:
        paginator = Paginator(dietas, 5)
        dietas = paginator.page(page)
    except:
        raise Http404
    

    data ={
        'entity': dietas,
        'paginator': paginator
    }
    return render(request, 'app/dieta/listar.html', data)

@permission_required('app.change_dieta')
def modificar_Dieta(request, id):
    dieta = get_object_or_404(Dieta, id=id)
    
    data ={
        'form': DietaForm(instance=dieta)
    }

    if request.method == 'POST':
        formulario = DietaForm(data= request.POST, instance=dieta)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect(to="listar_dietas")
        data["form"] =formulario


    return render(request, 'app/dieta/modificar.html',data )

@permission_required('app.delete_dieta')
def eliminar_Dieta(request, id):
    dieta= get_object_or_404(Dieta, id=id)
    dieta.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect(to="listar_dietas")

#Libredealimento CRUD

@permission_required('app.add_libre_de_alimento')
def agregar_Libre(request):
    
    data ={
        'form': LibreForm()
    }
    
    if request.method == 'POST':
        formulario = LibreForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Libre de alimento registrado")
        else:
            data["form"] = formulario 

    return render(request, 'app/libredealimento/agregar.html',data)

@permission_required('app.view_libre_de_alimento')
def listar_Libres(request):
    libres = LibreDeAlimento.objects.all()
    page = request.GET.get('page',1)

    try:
        paginator = Paginator(libres, 5)
        libres = paginator.page(page)
    except:
        raise Http404
    

    data ={
        'entity': libres,
        'paginator': paginator
    }
    return render(request, 'app/libredealimento/listar.html', data)

@permission_required('app.change_libre_de_alimento')
def modificar_Libre(request, id):
    libre = get_object_or_404(Dieta, id=id)
    
    data ={
        'form': LibreForm(instance=libre)
    }

    if request.method == 'POST':
        formulario = LibreForm(data= request.POST, instance=libre)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect(to="listar_libres")
        data["form"] =formulario


    return render(request, 'app/libredealimento/modificar.html',data )

@permission_required('app.delete_libre_de_alimento')
def eliminar_Libre(request, id):
    libre= get_object_or_404(LibreDeAlimento, id=id)
    libre.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect(to="listar_libres")


#AlimentoDieta CRUD

@permission_required('app.add_alimento_dieta')
def agregar_AlimentoDieta(request):
    
    data ={
        'form': AlimentoDietaForm()
    }
    
    if request.method == 'POST':
        formulario = AlimentoDietaForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Relacion Alimento-Dieta registrada")
        else:
            data["form"] = formulario 

    return render(request, 'app/alimentodieta/agregar.html',data)

@permission_required('app.view_alimento_dieta')
def listar_AlimentoDietas(request):
    alimentodietas = AlimentoDieta.objects.all()
    page = request.GET.get('page',1)

    try:
        paginator = Paginator(alimentodietas, 5)
        alimentodietas = paginator.page(page)
    except:
        raise Http404
    

    data ={
        'entity': alimentodietas,
        'paginator': paginator
    }
    return render(request, 'app/alimentodieta/listar.html', data)

@permission_required('app.change_alimento_dieta')
def modificar_AlimentoDieta(request, id):
    alimentodieta = get_object_or_404(AlimentoDieta, id=id)
    
    data ={
        'form': AlimentoDietaForm(instance=alimentodieta)
    }

    if request.method == 'POST':
        formulario = AlimentoDietaForm(data= request.POST, instance=alimentodieta)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect(to="listar_alimentodietas")
        data["form"] =formulario


    return render(request, 'app/alimentodieta/modificar.html',data )

@permission_required('app.delete_alimento_dieta')
def eliminar_AlimentoDieta(request, id):
    alimentodieta= get_object_or_404(AlimentoDieta, id=id)
    alimentodieta.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect(to="listar_alimentodietas")


#AlimentoLibrede CRUD

@permission_required('app.add_alimento_libre_de')
def agregar_AlimentoLibreDe(request):
    
     data ={
        'form': AlimentoLibreDeForm()
     }
    
     if request.method == 'POST':
         formulario = AlimentoLibreDeForm(data=request.POST)
         if formulario.is_valid():
             formulario.save()
             messages.success(request, "Relacion Alimento-LibreDeAlimento registrada")
         else:
             data["form"] = formulario 

     return render(request, 'app/alimentolibrede/agregar.html',data)

@permission_required('app.add_alimento_libre_de')
def listar_AlimentoLibreDe(request):
     alimentolibres = AlimentoLibreDe.objects.all()
     page = request.GET.get('page',1)

     try:
         paginator = Paginator(alimentolibres, 5)
         alimentolibres = paginator.page(page)
     except:
         raise Http404
    

     data ={
         'entity': alimentolibres,
         'paginator': paginator
     }
     return render(request, 'app/alimentolibrede/listar.html', data)

@permission_required('app.change_alimento_libre_de')
def modificar_AlimentoLibreDe(request, id):
     alimentolibre = get_object_or_404(AlimentoLibreDe, id=id)
    
     data ={
         'form': AlimentoLibreDeForm(instance=alimentolibre)
     }

     if request.method == 'POST':
         formulario = AlimentoLibreDeForm(data= request.POST, instance=alimentolibre)
         if formulario.is_valid():
             formulario.save()
             messages.success(request, "Modificado correctamente")
             return redirect(to="listar_alimentolibres")
         data["form"] =formulario


     return render(request, 'app/alimentolibrede/modificar.html',data )

@permission_required('app.delete_alimento_libre_de')
def eliminar_AlimentoLibreDe(request, id):
     alimentolibre= get_object_or_404(AlimentoLibreDe, id=id)
     alimentolibre.delete()
     messages.success(request, "Eliminado correctamente")
     return redirect(to="listar_alimentolibres")

def registro(request):
    data = {
        'form': CustomUserCreationForm
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password =formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            return redirect(to="home")
        data["form"]=formulario
    return render (request, 'registration/registro.html', data)



#Productos CRUD

@permission_required('app.add_producto')
def agregar_Producto(request):

    data ={
        'form': ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files =request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto registrado")
        else:
            data["form"] = formulario 

    return render(request, 'app/producto/agregar.html',data)

@permission_required('app.view_producto')
def listar_Productos(request):
    productos = Producto.objects.all()
    page = request.GET.get('page',1)

    try:
        paginator = Paginator(productos, 5)
        productos = paginator.page(page)
    except:
        raise Http404
    

    data ={
        'entity': productos,
        'paginator': paginator
    }
    return render(request, 'app/producto/listar.html', data)

@permission_required('app.change_producto')
def modificar_Producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    
    data ={
        'form': ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data= request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect(to="listar_productos")
        data["form"] =formulario


    return render(request, 'app/producto/modificar.html',data )

@permission_required('app.delete_producto')
def eliminar_Producto(request, id):
    producto= get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect(to="listar_productos")


def product_detail(request, product_id):
    # Aquí obtienes los datos nutricionales del producto (ejemplo)
    data = {
        'labels': ['Carbohidratos', 'Proteínas', 'Grasas'],
        'data': [30, 40, 30],  # Ejemplo de valores de porcentaje
    }
    return render(request, 'product_detail.html', {'data': data})

@login_required
def agregar_al_carrito(request, alimento_id):
    alimento = get_object_or_404(Alimento, id=alimento_id)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        item, item_creado = CarritoItem.objects.get_or_create(carrito=carrito, alimento=alimento)

        if not item_creado:
            item.cantidad += cantidad
        else:
            item.cantidad = cantidad

        item.save()

    return redirect('ver_carrito')

@login_required
def ver_carrito(request):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    items = CarritoItem.objects.filter(carrito=carrito)
    return render(request, 'app/carrito.html', {'items': items, 'carrito': carrito})

# def realizar_pedido(request):
#     carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
#     items = CarritoItem.objects.filter(carrito=carrito)
    
#     if not items:
#         return redirect('ver_carrito')

#     pedido = Pedido.objects.create(usuario=request.user, total=sum(item.alimento.precio * item.cantidad for item in items))

#     for item in items:
#         PedidoItem.objects.create(pedido=pedido, alimento=item.alimento, cantidad=item.cantidad, precio=item.alimento.precio)
#         item.delete()  # Vaciar el carrito después de realizar el pedido

#     carrito.delete()  # Eliminar el carrito después de realizar el pedido

#     return redirect('ver_pedido', pedido_id=pedido.id)
@login_required
def realizar_pedido(request):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    items = CarritoItem.objects.filter(carrito=carrito)
    
    if not items:
        return redirect('ver_carrito')

    pedido = Pedido.objects.create(usuario=request.user, total=sum(item.alimento.precio * item.cantidad for item in items))

    for item in items:
        PedidoItem.objects.create(pedido=pedido, alimento=item.alimento, cantidad=item.cantidad, precio=item.alimento.precio)
        item.delete()  # Vaciar el carrito después de realizar el pedido

    carrito.delete()  # Eliminar el carrito después de realizar el pedido

    return redirect('procesar_pago', pedido_id=pedido.id)

@login_required
def procesar_pago(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    # Crear un nuevo pago utilizando la SDK de PayPal
    pago = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('pago_exitoso', args=[pedido.id])),
            "cancel_url": request.build_absolute_uri(reverse('pago_cancelado'))
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": f"Pedido {pedido.id}",
                    "sku": f"pedido_{pedido.id}",
                    "price": str(pedido.total),
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": str(pedido.total),
                "currency": "USD"
            },
            "description": f"Pago del pedido {pedido.id}"
        }]
    })

    if pago.create():
        for link in pago.links:
            if link.rel == "approval_url":
                return redirect(link.href)
    else:
        return render(request, 'app/pago_error.html', {'error': pago.error})

@login_required
def pago_exitoso(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    pago_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    pago = paypalrestsdk.Payment.find(pago_id)

    if pago.execute({"payer_id": payer_id}):
        pedido.estado = 'pagado'
        pedido.save()
        
        items = PedidoItem.objects.filter(pedido=pedido)
        
        return render(request, 'app/pedido.html', {'pedido': pedido, 'items': items})
    else:
        return render(request, 'app/pago_error.html', {'error': pago.error})
@login_required
def pago_cancelado(request):
    return render(request, 'app/pago_cancelado.html')
@login_required
def ver_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    items = PedidoItem.objects.filter(pedido=pedido)
    return render(request, 'app/pedido.html', {'pedido': pedido, 'items': items})

# @login_required
# def ver_carrito(request):
#     carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
#     items = carrito.carritoitem_set.all()
#     total_precio = carrito.total_precio()
#     return render(request, 'app/carrito.html', {'carrito': carrito, 'items': items, 'total_precio': total_precio})

@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id)
    item.delete()
    return redirect('ver_carrito')

