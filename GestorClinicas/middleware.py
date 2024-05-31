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
        if request.path.startswith('/static/') or request.get_host() == "gestorclinicasdentales.shop" :
            return self.get_response(request)

        host = request.get_host()
        logger.debug(f"Host procesado: {host}")

        if hasattr(request, 'user') and request.user.is_authenticated:
            logger.debug(f"Usuario autenticado: {request.user.username}")

            try:
                domain = get_object_or_404(Domain, domain=host)
                logger.debug(f"Dominio encontrado: {domain.domain}")

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

        response = self.get_response(request)
        return response

