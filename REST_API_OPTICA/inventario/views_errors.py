from django.http import JsonResponse


def custom_404(request, exception=None):
    return JsonResponse({"detail": "No se encontró el recurso solicitado."}, status=404)


def custom_500(request):
    return JsonResponse(
        {"detail": "Error interno del servidor. Intenta de nuevo más tarde."}, status=500
    )
