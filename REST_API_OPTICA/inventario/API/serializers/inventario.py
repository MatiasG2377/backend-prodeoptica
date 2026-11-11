from rest_framework import serializers

from inventario.models import Categoria, Proveedor, Producto, ProductoProveedor, MovimientoInventario, Lote, Sucursal


class categoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class proveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'


# Serializador para el producto
class ProductoSerializer(serializers.ModelSerializer):
    # Incluyendo nombre de la categoría y sucursal en la representación
    categoria_nombre = serializers.CharField(source='categoria_producto.nombre_categoria', read_only=True)
    sucursal_nombre = serializers.CharField(source='sucursal_producto.nombre_sucursal', read_only=True)

    class Meta:
        model = Producto
        fields = '__all__'

    def to_internal_value(self, data):
        data_copy = data.copy() if hasattr(data, 'copy') else dict(data)

        # Normalizar sucursal_producto
        suc = data_copy.get('sucursal_producto')
        if suc is None or suc == '':
            first_suc = Sucursal.objects.first()
            data_copy['sucursal_producto'] = first_suc.id if first_suc else 1
        elif isinstance(suc, dict):
            data_copy['sucursal_producto'] = suc.get('id', 1)
        elif isinstance(suc, str) and not suc.isdigit():
            suc_obj = Sucursal.objects.filter(nombre_sucursal__iexact=suc).first() or Sucursal.objects.filter(nombre_sucursal__icontains=suc).first()
            data_copy['sucursal_producto'] = suc_obj.id if suc_obj else 1

        # Normalizar categoria_producto si viene como dict
        cat = data_copy.get('categoria_producto')
        if isinstance(cat, dict):
            data_copy['categoria_producto'] = cat.get('id')
        elif isinstance(cat, str) and not cat.isdigit():
            cat_obj = Categoria.objects.filter(nombre_categoria__iexact=cat).first() or Categoria.objects.filter(nombre_categoria__icontains=cat).first()
            if cat_obj:
                data_copy['categoria_producto'] = cat_obj.id

        return super().to_internal_value(data_copy)


# Serializador para la relación entre productos y proveedores
class ProductoProveedorSerializer(serializers.ModelSerializer):
    # Relación anidada para representación
    producto_nombre = serializers.CharField(source='producto_productoProveedor.nombre_producto', read_only=True)
    proveedor_nombre = serializers.CharField(source='proveedor_productoProveedor.nombre_proveedor', read_only=True)

    class Meta:
        model = ProductoProveedor
        fields = '__all__'


# Serializador para movimientos de inventario
class MovimientoInventarioSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto_movimientoInventario.nombre_producto', read_only=True)
    sucursal_nombre = serializers.CharField(source='sucursal_movimientoInventario.nombre_sucursal', read_only=True)

    class Meta:
        model = MovimientoInventario
        fields = '__all__'

    def to_internal_value(self, data):
        data_copy = data.copy() if hasattr(data, 'copy') else dict(data)

        # Mapear aliases estilo Kardex -> MovimientoInventario
        if 'producto_kardex' in data_copy and 'producto_movimientoInventario' not in data_copy:
            data_copy['producto_movimientoInventario'] = data_copy['producto_kardex']
        if 'tipo_kardex' in data_copy and 'tipo_movimientoInventario' not in data_copy:
            data_copy['tipo_movimientoInventario'] = data_copy['tipo_kardex']
        if 'cantidad_kardex' in data_copy and 'cantidad_movimientoInventario' not in data_copy:
            data_copy['cantidad_movimientoInventario'] = data_copy['cantidad_kardex']
        if 'referencia_kardex' in data_copy and 'motivo_movimientoInventario' not in data_copy:
            data_copy['motivo_movimientoInventario'] = data_copy['referencia_kardex']

        # Si el producto viene como objeto dict, extraer su id
        prod = data_copy.get('producto_movimientoInventario')
        if isinstance(prod, dict):
            data_copy['producto_movimientoInventario'] = prod.get('id')

        # Si la sucursal viene como objeto o no viene, asociar a la sucursal del producto o primera disponible
        suc = data_copy.get('sucursal_movimientoInventario')
        if suc is None or suc == '':
            prod_id = data_copy.get('producto_movimientoInventario')
            prod_obj = Producto.objects.filter(id=prod_id).first() if prod_id else None
            if prod_obj and prod_obj.sucursal_producto_id:
                data_copy['sucursal_movimientoInventario'] = prod_obj.sucursal_producto_id
            else:
                first_suc = Sucursal.objects.first()
                data_copy['sucursal_movimientoInventario'] = first_suc.id if first_suc else 1
        elif isinstance(suc, dict):
            data_copy['sucursal_movimientoInventario'] = suc.get('id', 1)

        # Normalizar tipo: capitalizar primera letra ("entrada" -> "Entrada", "salida" -> "Salida")
        tipo = data_copy.get('tipo_movimientoInventario')
        if isinstance(tipo, str) and tipo.capitalize() in ['Entrada', 'Salida']:
            data_copy['tipo_movimientoInventario'] = tipo.capitalize()

        return super().to_internal_value(data_copy)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Exponer también campos con nombres _kardex para compatibilidad con vistas y tablas de Kardex
        producto = getattr(instance, 'producto_movimientoInventario', None)
        costo_prod = float(producto.costo_producto or 0) if producto else 0.0
        cant = instance.cantidad_movimientoInventario or 0
        total_costo = round(costo_prod * cant, 2)
        stock_actual = producto.cantidad_producto if producto else 0

        data['producto_kardex'] = instance.producto_movimientoInventario_id
        data['tipo_kardex'] = instance.tipo_movimientoInventario
        data['cantidad_kardex'] = cant
        data['fecha_kardex'] = instance.fecha_movimientoInventario
        data['referencia_kardex'] = instance.motivo_movimientoInventario or ""
        data['costo_unitario_kardex'] = f"{costo_prod:.2f}"
        data['costo_total_kardex'] = f"{total_costo:.2f}"
        data['saldo_cantidad_kardex'] = stock_actual
        data['saldo_costo_kardex'] = f"{round(costo_prod * stock_actual, 2):.2f}"
        return data


# Serializador para lotes de productos
class LoteSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto_lote.nombre_producto', read_only=True)

    class Meta:
        model = Lote
        fields = '__all__'
