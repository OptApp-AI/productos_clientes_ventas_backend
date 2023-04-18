from django.contrib import admin
from .models import Producto, Cliente, PrecioCliente, Venta, ProductoVenta, Direccion, Empleado
# Register your models here.


admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(PrecioCliente)
admin.site.register(Venta)
admin.site.register(ProductoVenta)
admin.site.register(Direccion)
admin.site.register(Empleado)