from inventario.models import User


def crear_usuario(*, username, email, password, rol='Usuario', sucursal_usuario=None):
    return User.objects.create_user(
        username=username,
        email=email,
        password=password,
        rol=rol,
        sucursal_usuario=sucursal_usuario,
    )


def actualizar_usuario(*, user, password=None, **campos):
    for campo, valor in campos.items():
        setattr(user, campo, valor)
    if password:
        user.set_password(password)
    user.save()
    return user
