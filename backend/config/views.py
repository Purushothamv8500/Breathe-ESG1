from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render


def root(request):
    """
    Landing page at /
    JSON if Accept: application/json, else HTML for browsers.
    """
    frontend_url = settings.FRONTEND_URL or None

    if 'application/json' in request.headers.get('Accept', ''):
        return JsonResponse({
            'service': 'Breathe ESG Data Ingestion API',
            'status': 'running',
            'ui': frontend_url,
            'endpoints': {
                'dashboard': '/api/dashboard/',
                'records': '/api/records/',
                'ingest_sap': 'POST /api/ingest/sap/',
                'ingest_utility': 'POST /api/ingest/utility/',
                'ingest_travel': 'POST /api/ingest/travel/',
                'admin': '/admin/',
            },
        })

    return render(request, 'api_home.html', {
        'frontend_url': frontend_url,
    })
