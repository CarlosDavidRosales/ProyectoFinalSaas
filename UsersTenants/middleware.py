from datetime import date, timedelta

class TenantContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(request, 'tenant'):
            tenant = request.tenant
            today = date.today()
            
            # Verificar si la fecha límite ha pasado
            if tenant.fecha_limite < today:
                tenant.pagado = False
                tenant.save()
                
            request.pay = tenant.pagado
            request.date = tenant.fecha_limite
            print(f"Tenant pagado: {request.pay}, Fecha límite: {request.date}")
        return None

    def process_template_response(self, request, response):
        if hasattr(request, 'tenant'):
            if response.context_data is None:
                response.context_data = {}
            response.context_data['pay'] = request.tenant.pagado
            response.context_data['date'] = request.tenant.fecha_limite
            print(f"Contexto de la respuesta: {response.context_data}")
        return response
