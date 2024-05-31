import logging
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.contrib import messages
from Tenants.models import Domain, Client

logger = logging.getLogger(__name__)

class TenantAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Permitir acceso sin restricciones a la URL de inicio de sesión
        if request.path == "/" and request.get_host() == "gestorclinicasdentales.shop":
            return self.get_response(request)
        
        host = request.get_host()  # Obtener el nombre del host
        logger.debug(f"Host procesado: {host}")

        if hasattr(request, 'user') and request.user.is_authenticated:
            logger.debug(f"Usuario autenticado: {request.user.username}")

            # Intentar encontrar el dominio en la base de datos y verificar la relación con el usuario
            try:
                domain = get_object_or_404(Domain, domain=host)
                logger.debug(f"Dominio encontrado: {domain.domain}")

                # Verificar si el dominio está asociado al usuario autenticado a través del tenant
                tenant = domain.tenant
                if tenant.clinica != request.user:
                    logger.warning("Acceso denegado: No tiene permiso para este dominio.")
                    messages.warning(request, "Acceso denegado: No tiene permiso para el dominio al que intenta acceder, se regresa a su dominio correcto.")
                    print(request.user, tenant.clinica)
                    return HttpResponseRedirect(f"http://{request.user}.gestorclinicasdentales.shop")
            except Domain.DoesNotExist:
                logger.error(f"Error al buscar dominio: {host}")
                messages.warning(request, "Dominio inexistente, regístrese o autentifíquese para acceder.")
                return HttpResponseRedirect("http://gestorclinicasdentales.shop")
        else:
            logger.warning("Acceso denegado: usuario no autenticado")
            messages.warning(request, "Debes iniciar sesión para acceder a este dominio.")
            return HttpResponseRedirect("http://gestorclinicasdentales.shop")

        # Si todo está correcto, permitir la solicitud
        response = self.get_response(request)
        return response

class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()  # Obtener el nombre del host
        logger.debug(f"Host procesado: {host}")

        if host == "gestorclinicasdentales.shop":
            # Permitir que las solicitudes sigan su curso normal
            response = self.get_response(request)
            if response.status_code == 404:
                return HttpResponseRedirect("http://gestorclinicasdentales.shop")
            return response
        else:
            # Manejo de subdominios
            try:
                domain = get_object_or_404(Domain, domain=host)
                request.tenant = domain.tenant
            except Http404:
                return HttpResponseRedirect(f"http://{domain.tenant}.gestorclinicasdentales.shop")
        
        response = self.get_response(request)
        return response
