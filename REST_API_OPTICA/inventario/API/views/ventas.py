from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Sum
from decimal import Decimal

from inventario.models import (
    Laboratorio,
    Cliente,
    Paciente,
    FichaMedica,
    Venta,
    ArticuloVenta,
    Abono,
    Egreso,
)
from inventario.API.serializers import (
    LaboratorioSerializer,
    clienteSerializer,
    PacienteSerializer,
    FichaMedicaSerializer,
    VentaSerializer,
    ArticuloVentaSerializer,
    AbonoSerializer,
    EgresoSerializer,
)


class LaboratorioViewSet(viewsets.ModelViewSet):
    queryset = Laboratorio.objects.all()
    serializer_class = LaboratorioSerializer


class clienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = clienteSerializer

    def create(self, request, *args, **kwargs):
        # Permite crear cliente y paciente en una sola llamada si vienen campos de paciente
        data = request.data
        ci = data.get('ci_cliente') or data.get('ci') or data.get('ci_paciente')
        nombre = data.get('nombre_cliente') or data.get('nombres_paciente')
        apellido = data.get('apellido_cliente') or data.get('apellidos_paciente')
        correo = data.get('correo_cliente')
        telefono = data.get('telefono_cliente') or data.get('telefono_paciente')
        direccion = data.get('direccion_cliente') or data.get('direccion_paciente')
        info = data.get('informacion_cliente') or data.get('antecedentes_paciente')

        cliente = None
        if ci:
            cliente = Cliente.objects.filter(ci_cliente=ci).first()
        if not cliente and correo:
            cliente = Cliente.objects.filter(correo_cliente=correo).first()

        if cliente:
            if nombre: cliente.nombre_cliente = nombre
            if apellido: cliente.apellido_cliente = apellido
            if correo: cliente.correo_cliente = correo
            if telefono: cliente.telefono_cliente = telefono
            if direccion: cliente.direccion_cliente = direccion
            if info: cliente.informacion_cliente = info
            cliente.save()
        else:
            cliente = Cliente.objects.create(
                ci_cliente=ci or '9999999999',
                nombre_cliente=nombre or 'Consumidor Final',
                apellido_cliente=apellido or '',
                correo_cliente=correo,
                telefono_cliente=telefono or '',
                direccion_cliente=direccion or '',
                informacion_cliente=info or '',
            )

        # Si vienen datos de paciente, crear/actualizar Paciente también
        paciente = None
        if ci:
            paciente = Paciente.objects.filter(ci_paciente=ci).first()
        if paciente:
            if nombre: paciente.nombres_paciente = nombre
            if apellido: paciente.apellidos_paciente = apellido
            if telefono: paciente.telefono_paciente = telefono
            if direccion: paciente.direccion_paciente = direccion
            if data.get('fecha_nacimiento'): paciente.fecha_nacimiento = data.get('fecha_nacimiento')
            if data.get('ocupacion_paciente'): paciente.ocupacion_paciente = data.get('ocupacion_paciente')
            if data.get('antecedentes_paciente'): paciente.antecedentes_paciente = data.get('antecedentes_paciente')
            paciente.cliente = cliente
            paciente.save()
        else:
            paciente = Paciente.objects.create(
                cliente=cliente,
                ci_paciente=ci or cliente.ci_cliente,
                nombres_paciente=nombre or cliente.nombre_cliente,
                apellidos_paciente=apellido or (cliente.apellido_cliente or ''),
                fecha_nacimiento=data.get('fecha_nacimiento') or None,
                ocupacion_paciente=data.get('ocupacion_paciente') or '',
                direccion_paciente=direccion or cliente.direccion_cliente or '',
                telefono_paciente=telefono or cliente.telefono_cliente or '',
                antecedentes_paciente=data.get('antecedentes_paciente') or '',
            )

        fichas = FichaMedica.objects.filter(paciente=paciente).order_by('-fecha')
        fichas_data = FichaMedicaSerializer(fichas, many=True).data

        return Response({
            "cliente": clienteSerializer(cliente).data,
            "paciente": PacienteSerializer(paciente).data,
            "historial_fichas": fichas_data,
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def ci(self, request):
        ci_val = request.query_params.get('ci')
        if not ci_val:
            return Response({"detail": "Parámetro 'ci' requerido."}, status=status.HTTP_400_BAD_REQUEST)
        cliente = self.get_queryset().filter(ci_cliente=ci_val).first()
        if not cliente:
            return Response({"detail": "Cliente no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(cliente)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def buscar(self, request):
        ci_val = request.query_params.get('ci')
        term = request.query_params.get('q') or request.query_params.get('term')
        
        if ci_val:
            cliente = self.get_queryset().filter(ci_cliente=ci_val).first()
            paciente = Paciente.objects.filter(ci_paciente=ci_val).first()
            if not cliente and not paciente:
                return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
            
            if not paciente and cliente:
                paciente = Paciente.objects.filter(cliente=cliente).first()
            if not cliente and paciente:
                cliente = paciente.cliente

            fichas = FichaMedica.objects.filter(paciente=paciente).order_by('-fecha') if paciente else []
            fichas_data = FichaMedicaSerializer(fichas, many=True).data

            return Response({
                "cliente": clienteSerializer(cliente).data if cliente else None,
                "paciente": PacienteSerializer(paciente).data if paciente else None,
                "historial_fichas": fichas_data,
            })

        queryset = self.get_queryset()
        if term:
            clientes = queryset.filter(
                Q(nombre_cliente__icontains=term) |
                Q(apellido_cliente__icontains=term) |
                Q(ci_cliente__icontains=term)
            )
            return Response(self.get_serializer(clientes, many=True).data)
        return Response(self.get_serializer(queryset, many=True).data)

    @action(detail=False, methods=['get'], url_path='buscar-apellido')
    def buscar_apellido(self, request):
        apellido = request.query_params.get('apellido', '')
        pacientes = Paciente.objects.filter(apellidos_paciente__icontains=apellido)
        
        resultados = []
        for pac in pacientes:
            cli = pac.cliente or Cliente.objects.filter(ci_cliente=pac.ci_paciente).first()
            fichas = FichaMedica.objects.filter(paciente=pac).order_by('-fecha')
            resultados.append({
                "cliente": clienteSerializer(cli).data if cli else None,
                "paciente": PacienteSerializer(pac).data,
                "historial_fichas": FichaMedicaSerializer(fichas, many=True).data,
            })
        return Response(resultados)


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

    def list(self, request, *args, **kwargs):
        ci = request.query_params.get('ci')
        apellido = request.query_params.get('apellido')
        
        if ci:
            paciente = self.queryset.filter(ci_paciente=ci).first()
            if not paciente:
                return Response({"detail": "Paciente no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            fichas = FichaMedica.objects.filter(paciente=paciente).order_by('-fecha')
            return Response({
                "paciente": PacienteSerializer(paciente).data,
                "historial": FichaMedicaSerializer(fichas, many=True).data,
            })
        
        if apellido:
            pacientes = self.queryset.filter(apellidos_paciente__icontains=apellido)
            return Response(self.get_serializer(pacientes, many=True).data)

        return super().list(request, *args, **kwargs)


class FichaMedicaViewSet(viewsets.ModelViewSet):
    queryset = FichaMedica.objects.all().order_by('-fecha')
    serializer_class = FichaMedicaSerializer


class ventaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all().order_by('-fecha_venta')
    serializer_class = VentaSerializer

    @action(detail=False, methods=['get'])
    def fecha(self, request):
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        ventas = self.get_queryset()
        if fecha_inicio:
            ventas = ventas.filter(fecha_venta__date__gte=fecha_inicio)
        if fecha_fin:
            ventas = ventas.filter(fecha_venta__date__lte=fecha_fin)
        return Response(self.get_serializer(ventas, many=True).data)

    @action(detail=True, methods=['get'])
    def articulos(self, request, pk=None):
        venta = self.get_object()
        articulos = ArticuloVenta.objects.filter(venta_articuloVenta=venta)
        serializer = ArticuloVentaSerializer(articulos, many=True)
        return Response(serializer.data)


class articuloVentaViewSet(viewsets.ModelViewSet):
    queryset = ArticuloVenta.objects.all()
    serializer_class = ArticuloVentaSerializer


class AbonoViewSet(viewsets.ModelViewSet):
    queryset = Abono.objects.all().order_by('-fecha')
    serializer_class = AbonoSerializer

    @action(detail=False, methods=['get'])
    def fecha(self, request):
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        abonos = self.get_queryset()
        if fecha_inicio:
            abonos = abonos.filter(fecha__date__gte=fecha_inicio)
        if fecha_fin:
            abonos = abonos.filter(fecha__date__lte=fecha_fin)
        return Response(self.get_serializer(abonos, many=True).data)

    @action(detail=False, methods=['get'], url_path='por-venta/(?P<venta_id>[^/.]+)')
    def por_venta(self, request, venta_id=None):
        abonos = self.get_queryset().filter(venta_id=venta_id)
        return Response(self.get_serializer(abonos, many=True).data)

    @action(detail=False, methods=['get'], url_path='venta/(?P<venta_id>[^/.]+)')
    def venta(self, request, venta_id=None):
        abonos = self.get_queryset().filter(venta_id=venta_id)
        return Response(self.get_serializer(abonos, many=True).data)


class EgresoViewSet(viewsets.ModelViewSet):
    queryset = Egreso.objects.all().order_by('-fecha_egreso')
    serializer_class = EgresoSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(descripcion_egreso__icontains=search) |
                Q(categoria_egreso__icontains=search) |
                Q(metodo_pago_egreso__icontains=search)
            )
        return qs


class CierreCajaResumenView(APIView):
    """
    Devuelve los totales desglosados por método de pago para el Cierre de Caja
    """
    def get(self, request):
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')

        ventas_qs = Venta.objects.filter(estado_venta__in=['F', 'P'])
        abonos_qs = Abono.objects.all()
        egresos_qs = Egreso.objects.all()

        if fecha_inicio:
            ventas_qs = ventas_qs.filter(fecha_venta__date__gte=fecha_inicio)
            abonos_qs = abonos_qs.filter(fecha__date__gte=fecha_inicio)
            egresos_qs = egresos_qs.filter(fecha_egreso__date__gte=fecha_inicio)
        if fecha_fin:
            ventas_qs = ventas_qs.filter(fecha_venta__date__lte=fecha_fin)
            abonos_qs = abonos_qs.filter(fecha__date__lte=fecha_fin)
            egresos_qs = egresos_qs.filter(fecha_egreso__date__lte=fecha_fin)

        def suma_metodo(qs, field_metodo, field_monto, metodo):
            val = qs.filter(**{field_metodo: metodo}).aggregate(s=Sum(field_monto))['s']
            return float(val or Decimal('0.00'))

        v_ef = suma_metodo(ventas_qs, 'metodo_venta', 'total_venta', 'Efectivo')
        v_tr = suma_metodo(ventas_qs, 'metodo_venta', 'total_venta', 'Transferencia')
        v_tj = suma_metodo(ventas_qs, 'metodo_venta', 'total_venta', 'Tarjeta')
        v_tot = float(ventas_qs.aggregate(s=Sum('total_venta'))['s'] or Decimal('0.00'))

        a_ef = suma_metodo(abonos_qs, 'metodo_pago', 'monto', 'Efectivo')
        a_tr = suma_metodo(abonos_qs, 'metodo_pago', 'monto', 'Transferencia')
        a_tj = suma_metodo(abonos_qs, 'metodo_pago', 'monto', 'Tarjeta')
        a_tot = float(abonos_qs.aggregate(s=Sum('monto'))['s'] or Decimal('0.00'))

        e_ef = suma_metodo(egresos_qs, 'metodo_pago_egreso', 'monto_egreso', 'Efectivo')
        e_tr = suma_metodo(egresos_qs, 'metodo_pago_egreso', 'monto_egreso', 'Transferencia')
        e_tj = suma_metodo(egresos_qs, 'metodo_pago_egreso', 'monto_egreso', 'Tarjeta')
        e_tot = float(egresos_qs.aggregate(s=Sum('monto_egreso'))['s'] or Decimal('0.00'))

        return Response({
            "ventas": {"Efectivo": v_ef, "Transferencia": v_tr, "Tarjeta": v_tj},
            "abonos": {"Efectivo": a_ef, "Transferencia": a_tr, "Tarjeta": a_tj},
            "egresos": {"Efectivo": e_ef, "Transferencia": e_tr, "Tarjeta": e_tj},
            "ventas_total_general": v_tot,
            "abonos_total_general": a_tot,
            "egresos_total_general": e_tot,
        })
