from django.contrib import admin
from .models import Marca, Producto, Contacto,\
Dieta,Alimento,AlimentoDieta,AlimentoLibreDe,LibreDeAlimento,CategoriaAlimento
from .forms import ProductoForm

# Register your models here.


# class ProductoAdmin(admin.ModelAdmin):
#     list_display=["nombre", "precio", "nuevo", "marca"]
#     list_editable=["precio"]
#     search_fields=["nombre"]
#     list_filter =["marca", "nuevo"]
#     list_per_page =10
#     form = ProductoForm

# admin.site.register(Marca)
# admin.site.register(Producto, ProductoAdmin) 
admin.site.register(Contacto)

# ver admin tablas tienda
admin.site.register(Dieta)
admin.site.register(Alimento)
admin.site.register(AlimentoDieta)
admin.site.register(AlimentoLibreDe)
admin.site.register(LibreDeAlimento)
admin.site.register(CategoriaAlimento)
