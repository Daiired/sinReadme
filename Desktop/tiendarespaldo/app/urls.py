from django.urls import path, include
from django.shortcuts import redirect
from . import views
from .views import home, contacto, galeria, \
 registro, agregar_Alimento, listar_Alimentos,modificar_Alimento, eliminar_Alimento, agregar_Categoria,listar_Categorias, modificar_Categoria, eliminar_Categoria, agregar_Dieta, listar_Dietas, modificar_Dieta, eliminar_Dieta,agregar_Libre,listar_Libres,modificar_Libre, eliminar_Libre, agregar_AlimentoDieta, listar_AlimentoDietas, modificar_AlimentoDieta, eliminar_AlimentoDieta,descripcion_producto,agregar_AlimentoLibreDe,listar_AlimentoLibreDe,modificar_AlimentoLibreDe,eliminar_AlimentoLibreDe, ver_carrito, agregar_al_carrito,eliminar_del_carrito, realizar_pedido, ver_pedido, procesar_pago,pago_exitoso,pago_cancelado, index

def redirect_to_login(request):
    return redirect('/accounts/login/')

urlpatterns = [
    path('',index , name='index'),

    path('login/', redirect_to_login, name="redirect_to_login"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('home/', home, name="home"),
    path('contacto/', contacto, name="contacto"),
    path('galeria/', galeria, name="galeria"),
    path('registro/', registro,name="registro"),
    path('detalle/<int:id>/', descripcion_producto, name='detalle'),
    
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('agregar/<int:alimento_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('agregar_al_carrito/<int:alimento_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar/<int:item_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    
    path('realizar_pedido/', realizar_pedido, name='realizar_pedido'),
    path('pedido/<int:pedido_id>/', ver_pedido, name='ver_pedido'),

    path('procesar_pago/<int:pedido_id>/', procesar_pago, name='procesar_pago'),
    path('pago_exitoso/<int:pedido_id>/', pago_exitoso, name='pago_exitoso'),
    path('pago_cancelado/', pago_cancelado, name='pago_cancelado'),

    path('agregar-alimento/', agregar_Alimento, name="agregar_alimento"),
    path('listar-alimentos/', listar_Alimentos, name="listar_alimentos"),
    path('modificar-alimento/<id>/', modificar_Alimento, name="modificar_alimento"),
    path('eliminar-alimento/<id>/', eliminar_Alimento, name="eliminar_alimento"),

    path('agregar-categoria/', agregar_Categoria, name="agregar_categoria"),
    path('listar-categorias/', listar_Categorias, name="listar_categorias"),
    path('modificar-categoria/<id>/', modificar_Categoria, name="modificar_categoria"),
    path('eliminar-categoria/<id>/', eliminar_Categoria, name="eliminar_categoria"),

    path('agregar-dieta/', agregar_Dieta, name="agregar_dieta"),
    path('listar-dietas/', listar_Dietas, name="listar_dietas"),
    path('modificar-dieta/<id>/', modificar_Dieta, name="modificar_dieta"),
    path('eliminar-dieta/<id>/', eliminar_Dieta, name="eliminar_dieta"),

    path('agregar-libre/', agregar_Libre, name="agregar_libre"),
    path('listar-libres/', listar_Libres, name="listar_libres"),
    path('modificar-libre/<id>/', modificar_Libre, name="modificar_libre"),
    path('eliminar-libre/<id>/', eliminar_Libre, name="eliminar_libre"),

    path('agregar-alimentodieta/', agregar_AlimentoDieta, name="agregar_alimentodieta"),
    path('listar-alimentodietas/', listar_AlimentoDietas, name="listar_alimentodietas"),
    path('modificar-alimentodieta/<id>/', modificar_AlimentoDieta, name="modificar_alimentodieta"),
    path('eliminar-alimentodieta/<id>/', eliminar_AlimentoDieta, name="eliminar_alimentodieta"),

    path('agregar-alimentolibre/', agregar_AlimentoLibreDe, name="agregar_alimentolibre"),
    path('listar-alimentolibres/', listar_AlimentoLibreDe, name="listar_alimentolibres"),
    path('modificar-alimentolibre/<id>/', modificar_AlimentoLibreDe, name="modificar_alimentolibre"),
    path('eliminar-alimentolibre/<id>/', eliminar_AlimentoLibreDe, name="eliminar_alimentolibre"),

]

