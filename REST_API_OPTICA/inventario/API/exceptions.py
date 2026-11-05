from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    """Garantiza que toda excepcion de una vista DRF devuelva JSON, nunca HTML."""
    response = drf_exception_handler(exc, context)
    if response is not None:
        return response

    return Response(
        {"detail": "Error interno del servidor. Intenta de nuevo más tarde."},
        status=500,
    )
