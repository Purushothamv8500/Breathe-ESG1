"""Multi-tenant resolution from request headers."""

from django.conf import settings
from rest_framework.exceptions import NotFound, ValidationError

from tenants.models import Tenant

CLIENT_ID_HEADER = 'HTTP_X_CLIENT_ID'
DEFAULT_DEV_CLIENT_ID = 'acme'


def get_client_id_from_request(request):
    client_id = request.META.get(CLIENT_ID_HEADER) or request.query_params.get('client_id')
    if not client_id and hasattr(request, 'data') and request.data:
        client_id = request.data.get('client_id')
    client_id = (client_id or '').strip()
    if not client_id and settings.DEBUG:
        return DEFAULT_DEV_CLIENT_ID
    return client_id


def get_tenant_from_request(request):
    client_id = get_client_id_from_request(request)
    if not client_id:
        raise ValidationError({
            'client_id': (
                'Required. Pass header X-Client-Id: acme (or globex), '
                'or add ?client_id=acme to the URL for browser testing.'
            ),
        })
    try:
        return Tenant.objects.get(client_id=client_id)
    except Tenant.DoesNotExist:
        raise NotFound(f'Tenant with client_id="{client_id}" not found.')
