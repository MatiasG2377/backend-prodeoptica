import random
from decimal import Decimal
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from inventario.models import (
    Sucursal,
    User,
    Categoria,
    Proveedor,
    Laboratorio,
    Producto,
    ProductoProveedor,
    MovimientoInventario,
    Lote,
    Cliente,
    Paciente,
    FichaMedica,
    Venta,
    ArticuloVenta,
    Abono,
    Egreso,
)


class Command(BaseCommand):
    help = "Puebla la base de datos con datos completos y realistas para el sistema de óptica"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Iniciando carga de seeders para Prodeóptica..."))

        # 1. SUCURSALES
        sucursales_data = [
            {
                "nombre_sucursal": "Matriz - Centro Histórico",
                "direccion_sucursal": "Chile 1050 y Guayaquil, Quito",
                "telefono_sucursal": "022584120",
                "gerente_sucursal": "Matías Gamboa",
            },
            {
                "nombre_sucursal": "Sucursal Norte - CCI",
                "direccion_sucursal": "Av. Amazonas y Naciones Unidas, CCI Local 45",
                "telefono_sucursal": "022456789",
                "gerente_sucursal": "Dra. Valentina Castro",
            },
            {
                "nombre_sucursal": "Sucursal Cumbayá",
                "direccion_sucursal": "Av. Interoceánica, Paseo San Francisco Nivel 1",
                "telefono_sucursal": "022891234",
                "gerente_sucursal": "Dr. Fernando Andrade",
            },
        ]
        sucursales = []
        for s_data in sucursales_data:
            s, _ = Sucursal.objects.get_or_create(
                nombre_sucursal=s_data["nombre_sucursal"], defaults=s_data
            )
            sucursales.append(s)
        self.stdout.write(self.style.SUCCESS(f"  [OK] {len(sucursales)} Sucursales configuradas"))

        # 2. USUARIOS
        usuarios_data = [
            {
                "username": "admin",
                "email": "admin@prodeoptica.com",
                "first_name": "Admin",
                "last_name": "Prodeóptica",
                "rol": "Administrador",
                "is_staff": True,
                "is_superuser": True,
                "sucursal": sucursales[0],
            },
            {
                "username": "gerente_norte",
                "email": "gerente.norte@prodeoptica.com",
                "first_name": "Valentina",
                "last_name": "Castro",
                "rol": "Gerente",
                "is_staff": True,
                "is_superuser": False,
                "sucursal": sucursales[1],
            },
            {
                "username": "vendedor1",
                "email": "vendedor1@prodeoptica.com",
                "first_name": "Carlos",
                "last_name": "Pérez",
                "rol": "Usuario",
                "is_staff": False,
                "is_superuser": False,
                "sucursal": sucursales[0],
            },
        ]
        users_dict = {}
        for u_data in usuarios_data:
            user, _ = User.objects.get_or_create(username=u_data["username"])
            user.email = u_data["email"]
            user.first_name = u_data["first_name"]
            user.last_name = u_data["last_name"]
            user.rol = u_data["rol"]
            user.is_staff = u_data["is_staff"]
            user.is_superuser = u_data["is_superuser"]
            user.sucursal_usuario = u_data["sucursal"]
            user.set_password("admin")
            user.save()
            users_dict[u_data["username"]] = user
        self.stdout.write(self.style.SUCCESS("  [OK] Usuarios base creados (pass: admin)"))

        # 3. CATEGORÍAS
        categorias_data = [
            ("Armazones Oftálmicos", "Armazones de acetato, titanio y metal para lunas graduadas", 10),
            ("Gafas de Sol", "Gafas solares polarizadas con protección UV400", 9),
            ("Lentes de Contacto", "Lentes blandos, tóricos, multifocales y cosméticos", 8),
            ("Lunas y Cristales", "Cristales monofocales, bifocales y progresivos con antireflejo", 7),
            ("Soluciones y Gotas", "Líquidos limpiadores, desinfectantes y lágrimas artificiales", 6),
            ("Accesorios y Limpieza", "Estuches rígidos, cordones, paños de microfibra y sprays", 5),
        ]
        cat_dict = {}
        for nom, desc, rel in categorias_data:
            cat, _ = Categoria.objects.get_or_create(
                nombre_categoria=nom,
                defaults={"descripcion_categoria": desc, "relevancia_categoria": rel, "activo_categoria": True},
            )
            cat_dict[nom] = cat
        self.stdout.write(self.style.SUCCESS(f"  [OK] {len(cat_dict)} Categorías creadas"))

        # 4. PROVEEDORES
        proveedores_data = [
            ("Luxottica Ecuador S.A.", "luxottica@optica.ec", "0991234567", "Distribuidor oficial Ray-Ban, Oakley, Vogue", "Guayaquil"),
            ("Essilor Óptica Mayorista", "ventas@essilor.ec", "0987654321", "Laboratorio de lunas oftálmicas Crizal y Varilux", "Quito"),
            ("Bausch & Lomb Ecuador", "pedidos@bausch.ec", "0995551234", "Lentes de contacto PureVision y soluciones Biotrue", "Cuenca"),
            ("Safilo Group Andina", "contacto@safilo.ec", "0984443322", "Marcas Carrera, Tommy Hilfiger, Polaroid", "Quito"),
            ("CooperVision Ecuador", "info@coopervision.ec", "0993332211", "Lentes Biofinity, Clariti y MyDay", "Quito"),
            ("Marchon Eyewear", "ventas@marchon.ec", "0981112233", "Lacoste, Calvin Klein, Nike Vision", "Guayaquil"),
        ]
        prov_dict = {}
        for nom, mail, telf, info, dir_p in proveedores_data:
            prov = Proveedor.objects.filter(correo_proveedor=mail).first() or Proveedor.objects.filter(nombre_proveedor=nom).first()
            if prov:
                prov.nombre_proveedor = nom
                prov.correo_proveedor = mail
                prov.telefono_proveedor = telf
                prov.informacion_proveedor = info
                prov.direccion_proveedor = dir_p
                prov.save()
            else:
                prov = Proveedor.objects.create(
                    nombre_proveedor=nom,
                    correo_proveedor=mail,
                    telefono_proveedor=telf,
                    informacion_proveedor=info,
                    direccion_proveedor=dir_p,
                )
            prov_dict[nom] = prov
        self.stdout.write(self.style.SUCCESS(f"  [OK] {len(prov_dict)} Proveedores registrados"))

        # 5. LABORATORIOS
        laboratorios_data = [
            ("Laboratorio Óptico Andina", "Av. 12 de Octubre y Lincoln, Quito", "022567890"),
            ("Laboratorio Lentes del Ecuador", "Av. Francisco de Orellana, Guayaquil", "042890123"),
            ("Laboratorio Especializado Crizal", "Av. Remigio Crespo, Cuenca", "072814567"),
        ]
        laboratorios = []
        for nom_lab, dir_lab, tel_lab in laboratorios_data:
            lab, _ = Laboratorio.objects.get_or_create(
                nombre_laboratorio=nom_lab,
                defaults={"direccion_laboratorio": dir_lab, "telefono_laboratorio": tel_lab},
            )
            laboratorios.append(lab)
        self.stdout.write(self.style.SUCCESS(f"  [OK] {len(laboratorios)} Laboratorios registrados"))

        # 6. PRODUCTOS
        productos_seed = [
            # Gafas de Sol
            ("Ray-Ban Aviator Classic RB3025", "Gafas de Sol", "Ray-Ban", 165.00, 95.00, 18, 4, 35, "Gafas de sol polarizadas doradas con lente verde clásico G-15."),
            ("Ray-Ban Wayfarer Classic RB2140", "Gafas de Sol", "Ray-Ban", 155.00, 88.00, 14, 3, 30, "Montura de acetato negro brillante con cristales polarizados."),
            ("Oakley Holbrook Matte Black Prizm", "Gafas de Sol", "Oakley", 145.00, 80.00, 15, 3, 25, "Diseño clásico con lentes Prizm Grey de alto contraste."),
            ("Oakley Frogskins Crystal Clear", "Gafas de Sol", "Oakley", 125.00, 68.00, 10, 2, 20, "Diseño retro de los 80 con tecnología moderna O-Matter."),
            # Armazones Oftálmicos
            ("Armazón Vogue Eyewear VO5276", "Armazones Oftálmicos", "Vogue", 98.00, 50.00, 22, 5, 40, "Armazón cat-eye femenino en acetato ligero color carey."),
            ("Armazón Carrera 8824 Titanium", "Armazones Oftálmicos", "Carrera", 120.00, 65.00, 12, 3, 25, "Montura rectangular de titanio ultra liviana y resistente."),
            ("Armazón Tommy Hilfiger TH1789", "Armazones Oftálmicos", "Tommy Hilfiger", 110.00, 58.00, 16, 4, 30, "Montura moderna semi-al aire en metal azul marino."),
            ("Armazón Silhouette Titan Minimal Art", "Armazones Oftálmicos", "Silhouette", 240.00, 130.00, 8, 2, 15, "El armazón sin aros más ligero del mundo en titanio puro."),
            # Lentes de Contacto
            ("Lentes de Contacto Acuvue Oasys (Caja 6)", "Lentes de Contacto", "Johnson & Johnson", 42.00, 24.00, 45, 10, 80, "Lentes quincenales de hidrogel de silicona con Hydraclear Plus."),
            ("Lentes Air Optix Plus HydraGlyde (Caja 6)", "Lentes de Contacto", "Alcon", 38.00, 21.00, 35, 8, 60, "Lentes mensuales con tecnología SmartShield contra depósitos."),
            ("Lentes Biofinity Toric para Astigmatismo", "Lentes de Contacto", "CooperVision", 48.00, 28.00, 25, 6, 50, "Diseño de geometría optimizada para visión nítida y estable."),
            # Lunas y Cristales
            ("Lunas Antirreflejo Crizal Sapphire HR", "Lunas y Cristales", "Essilor", 85.00, 40.00, 50, 10, 100, "Máxima transparencia con protección contra rayaduras y polvo."),
            ("Lunas Fotocromáticas Transitions Gen 8", "Lunas y Cristales", "Essilor", 130.00, 70.00, 30, 8, 60, "Oscurecimiento ultrarrápido al sol y total claridad en interiores."),
            ("Lunas Blue Light Filter UV400", "Lunas y Cristales", "Essilor", 65.00, 30.00, 40, 10, 80, "Filtro esencial contra luz azul de pantallas y fatiga visual."),
            # Soluciones y Gotas
            ("Solución Multipropósito Biotrue 300ml", "Soluciones y Gotas", "Bausch & Lomb", 14.50, 8.00, 60, 15, 120, "Inspirada en la biología de los ojos con pH equilibrado."),
            ("Lágrimas Artificiales Systane Ultra 10ml", "Soluciones y Gotas", "Alcon", 16.00, 9.50, 40, 10, 80, "Alivio inmediato del ojo seco y lubricación ocular prolongada."),
            # Accesorios y Limpieza
            ("Kit Limpieza Anti-Empañante OptiFog", "Accesorios y Limpieza", "Essilor", 8.00, 4.00, 50, 10, 100, "Spray activador y paño especial de microfibra."),
            ("Estuche Rígido Térmico Premium", "Accesorios y Limpieza", "Luxottica", 6.50, 3.00, 45, 10, 90, "Protección total anti-impacto con interior aterciopelado."),
        ]

        productos = []
        for nom, cat_nom, marca, pvp, costo, cant, mini, maxi, desc in productos_seed:
            prod, _ = Producto.objects.get_or_create(
                nombre_producto=nom,
                defaults={
                    "categoria_producto": cat_dict[cat_nom],
                    "sucursal_producto": random.choice(sucursales),
                    "pvp_producto": Decimal(str(pvp)),
                    "costo_producto": Decimal(str(costo)),
                    "cantidad_producto": cant,
                    "minimo_producto": mini,
                    "maximo_producto": maxi,
                    "marca_producto": marca,
                    "estado_producto": "Disponible",
                    "descripcion_producto": desc,
                    "ultima_venta_producto": timezone.now() - timedelta(days=random.randint(1, 15)),
                },
            )
            productos.append(prod)
        self.stdout.write(self.style.SUCCESS(f"  [OK] {len(productos)} Productos creados"))

        # 7. PRODUCTO - PROVEEDOR
        prod_prov_pairs = [
            ("Ray-Ban", "Luxottica Ecuador S.A."),
            ("Oakley", "Luxottica Ecuador S.A."),
            ("Vogue", "Luxottica Ecuador S.A."),
            ("Carrera", "Safilo Group Andina"),
            ("Tommy Hilfiger", "Safilo Group Andina"),
            ("Silhouette", "Marchon Eyewear"),
            ("Johnson & Johnson", "Bausch & Lomb Ecuador"),
            ("Alcon", "Bausch & Lomb Ecuador"),
            ("CooperVision", "CooperVision Ecuador"),
            ("Essilor", "Essilor Óptica Mayorista"),
            ("Bausch & Lomb", "Bausch & Lomb Ecuador"),
        ]

        rel_count = 0
        for prod in productos:
            for marca_key, prov_name in prod_prov_pairs:
                if marca_key in prod.marca_producto:
                    prov = prov_dict.get(prov_name)
                    if prov:
                        ProductoProveedor.objects.get_or_create(
                            producto_productoProveedor=prod,
                            proveedor_productoProveedor=prov,
                            defaults={
                                "costo_productoProveedor": prod.costo_producto,
                                "tiempo_entrega_productoProveedor": random.randint(2, 5),
                            },
                        )
                        rel_count += 1
                        break
        self.stdout.write(self.style.SUCCESS(f"  [OK] {rel_count} Relaciones Producto-Proveedor vinculadas"))

        # 8. LOTES
        lote_count = 0
        for prod in productos:
            if prod.categoria_producto.nombre_categoria in ["Lentes de Contacto", "Soluciones y Gotas"]:
                exp_date = date.today() + timedelta(days=random.randint(300, 720))
            else:
                exp_date = None
            Lote.objects.get_or_create(
                producto_lote=prod,
                cantidad_lote=prod.cantidad_producto,
                defaults={"fecha_caducidad_lote": exp_date},
            )
            lote_count += 1
        self.stdout.write(self.style.SUCCESS(f"  [OK] {lote_count} Lotes registrados"))

        # 9. CLIENTES Y PACIENTES
        clientes_data = [
            ("1720345678", "Carlos", "Mendoza", "carlos.mendoza@email.com", "0998877665", "Av. 10 de Agosto y Colón, Edif. Torre Azul", "Paciente regular con prescripción de miopía.", "1988-05-14", "Ingeniero Civil", "Astigmatismo leve en ojo izquierdo."),
            ("0918273645", "Ana María", "Paredes", "ana.paredes@email.com", "0987654321", "Av. Shyris y Portugal, Dpto 4B", "Usa lentes de contacto Acuvue Oasys.", "1994-09-22", "Diseñadora Gráfica", "Uso prolongado de pantallas."),
            ("1719283746", "Luis", "Morales", "luis.morales@email.com", "0991122334", "Cumbayá, Paseo San Francisco Casa 12", "Cliente VIP, compra monturas de titanio.", "1979-11-30", "Abogado", "Presbicia progresiva."),
            ("1709876543", "Elena", "Gómez", "elena.gomez@email.com", "0982233445", "La Floresta, Guipúzcoa E14-20", "Chequeo visual anual cada diciembre.", "1985-03-17", "Docente Universitaria", "Cirugía refractiva previa en 2018."),
            ("0102030405", "Jorge", "Salgado", "jorge.salgado@email.com", "0994455667", "Av. América y Rumipamba", "Prefiere lentes progresivos Transitions.", "1968-07-08", "Contador Auditor", "Hipertensión controlada."),
            ("1716253489", "Sofía", "Enríquez", "sofia.enriquez@email.com", "0986677889", "Tumbaco, Vía Intervalles Km 3", "Sensible a la luz de pantallas de oficina.", "1998-12-05", "Desarrolladora Web", "Fatiga visual al final de la jornada."),
            ("0923456781", "Mateo", "Valdivieso", "mateo.v@email.com", "0997788990", "González Suárez y Coruña", "Atleta aficionado, usa gafas polarizadas Oakley.", "2001-04-19", "Estudiante de Medicina", "Sin antecedentes patológicos oculares."),
            ("1711223344", "Carmen", "Jaramillo", "carmen.j@email.com", "0989900112", "Villa Flora, Alonso de Angulo", "Control para presbicia con lunas bifocales.", "1960-01-25", "Jubilada", "Ojo seco moderado."),
        ]
        clientes = []
        pacientes = []
        for ci, nom, ape, mail, telf, dir_c, info, fnac, ocup, antec in clientes_data:
            cli = Cliente.objects.filter(ci_cliente=ci).first() or Cliente.objects.filter(correo_cliente=mail).first()
            if cli:
                cli.ci_cliente = ci
                cli.nombre_cliente = nom
                cli.apellido_cliente = ape
                cli.correo_cliente = mail
                cli.telefono_cliente = telf
                cli.direccion_cliente = dir_c
                cli.informacion_cliente = info
                cli.save()
            else:
                cli = Cliente.objects.create(
                    ci_cliente=ci,
                    nombre_cliente=nom,
                    apellido_cliente=ape,
                    correo_cliente=mail,
                    telefono_cliente=telf,
                    direccion_cliente=dir_c,
                    informacion_cliente=info,
                )
            clientes.append(cli)

            pac = Paciente.objects.filter(ci_paciente=ci).first()
            if pac:
                pac.nombres_paciente = nom
                pac.apellidos_paciente = ape
                pac.fecha_nacimiento = fnac
                pac.ocupacion_paciente = ocup
                pac.direccion_paciente = dir_c
                pac.telefono_paciente = telf
                pac.antecedentes_paciente = antec
                pac.cliente = cli
                pac.save()
            else:
                pac = Paciente.objects.create(
                    cliente=cli,
                    ci_paciente=ci,
                    nombres_paciente=nom,
                    apellidos_paciente=ape,
                    fecha_nacimiento=fnac,
                    ocupacion_paciente=ocup,
                    direccion_paciente=dir_c,
                    telefono_paciente=telf,
                    antecedentes_paciente=antec,
                )
            pacientes.append(pac)
        self.stdout.write(self.style.SUCCESS(f"  [OK] {len(clientes)} Clientes y {len(pacientes)} Pacientes vinculados"))

        # 10. FICHAS MÉDICAS
        FichaMedica.objects.all().delete()
        fichas_creadas = 0
        admin_user = users_dict.get("admin")
        for pac in pacientes[:6]:
            opt_data = {
                "rx_distancia_od_av": "20/25",
                "rx_distancia_od_esfera": "-1.50",
                "rx_distancia_od_cilindro": "-0.50",
                "rx_distancia_od_eje": "90",
                "rx_distancia_od_dnp": "31",
                "rx_distancia_oi_av": "20/20",
                "rx_distancia_oi_esfera": "-1.75",
                "rx_distancia_oi_cilindro": "-0.75",
                "rx_distancia_oi_eje": "85",
                "rx_distancia_oi_dnp": "32",
                "rx_add_od_av": "20/20",
                "rx_add_od_esfera": "+1.50",
                "rx_add_od_cilindro": "",
                "rx_add_od_eje": "",
                "rx_add_od_dnp": "30",
                "rx_add_oi_av": "20/20",
                "rx_add_oi_esfera": "+1.50",
                "rx_add_oi_cilindro": "",
                "rx_add_oi_eje": "",
                "rx_add_oi_dnp": "30",
                "diagnostico": "Miopía y astigmatismo miópico compuesto.",
                "tipo_lente": "Monofocal Digital con Antirreflejo",
                "material": "Policarbonato 1.59",
                "observaciones": "Control visual sugerido en 12 meses.",
            }
            FichaMedica.objects.create(
                paciente=pac,
                usuario=admin_user,
                sucursal=sucursales[0],
                datos_opticos=opt_data,
            )
            fichas_creadas += 1
        self.stdout.write(self.style.SUCCESS(f"  [OK] {fichas_creadas} Fichas Médicas ópticas creadas"))

        # 11. VENTAS Y ARTÍCULOS DE VENTA
        Abono.objects.all().delete()
        Venta.objects.all().delete()
        ventas_creadas = 0
        articulos_creados = 0
        abonos_creados = 0

        metodos = ["Efectivo", "Transferencia", "Tarjeta"]

        for i in range(1, 11):
            cli = random.choice(clientes)
            suc = random.choice(sucursales)
            lab = random.choice(laboratorios)
            estado = "F" if i <= 7 else "P"
            metodo = random.choice(metodos)
            fecha = timezone.now() - timedelta(days=random.randint(1, 14), hours=random.randint(1, 8))

            venta = Venta.objects.create(
                cliente_venta=cli,
                sucursal_venta=suc,
                usuario_venta=admin_user,
                laboratorio_venta=lab,
                orden_laboratorio=f"LAB-{random.randint(1000, 9999)}",
                orden_trabajo=f"OT-{random.randint(2000, 8999)}",
                metodo_venta=metodo,
                fecha_venta=fecha,
                estado_venta=estado,
                total_venta=Decimal("0.00"),
            )

            items = random.sample(productos, 2)
            total_venta = Decimal("0.00")
            for prod in items:
                cant = random.randint(1, 2)
                precio = prod.pvp_producto
                descuento = Decimal("5.00") if cant > 1 else Decimal("0.00")
                subtotal = (precio * cant) - descuento

                ArticuloVenta.objects.create(
                    venta_articuloVenta=venta,
                    producto_articuloVenta=prod,
                    cantidad_articuloVenta=cant,
                    pvp_articuloVenta=precio,
                    descuento_articuloVenta=descuento,
                )
                total_venta += subtotal
                articulos_creados += 1

                # Kardex de Salida
                MovimientoInventario.objects.create(
                    producto_movimientoInventario=prod,
                    sucursal_movimientoInventario=suc,
                    tipo_movimientoInventario="Salida",
                    cantidad_movimientoInventario=cant,
                    motivo_movimientoInventario=f"Venta #{venta.id} a {cli.nombre_cliente}",
                )

            venta.total_venta = total_venta
            venta.save()
            ventas_creadas += 1

            # Crear Abonos para ventas pendientes o con saldo
            if estado == "P":
                monto_abono = round(total_venta * Decimal("0.40"), 2)
                Abono.objects.create(
                    venta=venta,
                    cliente=cli,
                    monto=monto_abono,
                    metodo_pago=metodo,
                    completado=False,
                )
                abonos_creados += 1
            elif i % 3 == 0:
                # Venta finalizada que tuvo abonos completados
                monto_abono1 = round(total_venta * Decimal("0.50"), 2)
                monto_abono2 = total_venta - monto_abono1
                Abono.objects.create(
                    venta=venta,
                    cliente=cli,
                    monto=monto_abono1,
                    metodo_pago="Efectivo",
                    completado=False,
                )
                Abono.objects.create(
                    venta=venta,
                    cliente=cli,
                    monto=monto_abono2,
                    metodo_pago="Transferencia",
                    completado=True,
                )
                abonos_creados += 2

        self.stdout.write(self.style.SUCCESS(f"  [OK] {ventas_creadas} Ventas, {articulos_creados} Artículos y {abonos_creados} Abonos registrados"))

        # 12. EGRESOS DE CAJA
        Egreso.objects.all().delete()
        egresos_seed = [
            (Decimal("120.00"), "Pago de servicios básicos luz y agua mensual", "Servicios básicos", "Efectivo"),
            (Decimal("450.00"), "Arriendo de local comercial sucursal CCI", "Arriendo", "Transferencia"),
            (Decimal("65.00"), "Compra de suministros de limpieza y cafetería", "Suministros", "Efectivo"),
            (Decimal("85.00"), "Servicio técnico y calibración de refractómetro", "Mantenimiento", "Transferencia"),
            (Decimal("35.00"), "Papelería, facturas y rollos térmicos para POS", "Suministros", "Efectivo"),
            (Decimal("95.00"), "Publicidad local en redes sociales y volantes", "Publicidad", "Tarjeta"),
        ]
        egresos_creados = 0
        for monto_e, desc_e, cat_e, met_e in egresos_seed:
            Egreso.objects.create(
                monto_egreso=monto_e,
                descripcion_egreso=desc_e,
                categoria_egreso=cat_e,
                metodo_pago_egreso=met_e,
                usuario_egreso=admin_user,
                sucursal_egreso=random.choice(sucursales),
            )
            egresos_creados += 1
        self.stdout.write(self.style.SUCCESS(f"  [OK] {egresos_creados} Egresos de caja registrados"))

        # 13. KARDEX INICIAL (MOVIMIENTOS DE ENTRADA)
        mov_in_count = 0
        for prod in productos:
            MovimientoInventario.objects.create(
                producto_movimientoInventario=prod,
                sucursal_movimientoInventario=prod.sucursal_producto,
                tipo_movimientoInventario="Entrada",
                cantidad_movimientoInventario=prod.cantidad_producto + 20,
                motivo_movimientoInventario="Recepción de pedido inicial de proveedor",
            )
            mov_in_count += 1
        self.stdout.write(self.style.SUCCESS(f"  [OK] {mov_in_count} Entradas de inventario inicial registradas en Kardex"))

        self.stdout.write(self.style.NOTICE("\n================================================"))
        self.stdout.write(self.style.SUCCESS(" SEEDERS COMPLETADOS CON EXITO PARA TODO EL SISTEMA"))
        self.stdout.write(self.style.NOTICE("================================================\n"))
