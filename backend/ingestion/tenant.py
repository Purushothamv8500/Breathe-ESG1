"""Multi-tenant resolution from request headers."""

from rest_framework.exceptions import NotFound, ValidationError

from tenants.models import Tenant

CLIENT_ID_HEADER = 'HTTP_X_CLIENT_ID'


def get_client_id_from_request(request):
    client_id = request.META.get(CLIENT_ID_HEADER) or request.query_params.get('client_id')
    if not client_id and hasattr(request, 'data') and request.data:
        client_id = request.data.get('client_id')
    return (client_id or '').strip()


def get_tenant_from_request(request):
    client_id = get_client_id_from_request(request)
    if not client_id:
        raise ValidationError({'client_id': 'Required. Pass X-Client-Id header or client_id query/body param.'})
    try:
        return Tenant.objects.get(client_id=client_id)
    except Tenant.DoesNotExist:
        raise NotFound(f'Tenant with client_id="{client_id}" not found.')
