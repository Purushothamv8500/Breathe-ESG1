from django.http import JsonResponse
from django.shortcuts import render


def root(request):
    """
    Landing page at http://127.0.0.1:8001/
    JSON if Accept: application/json, else HTML for browsers.
    """
    if 'application/json' in request.headers.get('Accept', ''):
        return JsonResponse({
            'service': 'Breathe ESG Data Ingestion API',
            'status': 'running',
            'ui': 'http://127.0.0.1:5173',
            'endpoints': {
                'dashboard': '/api/dashboard/',
                'records': '/api/records/',
                'ingest_sap': 'POST /api/ingest/sap/',
                'ingest_utility': 'POST /api/ingest/utility/',
                'ingest_travel': 'POST /api/ingest/travel/',
                'admin': '/admin/',
            },
        })

    return render(request, 'api_home.html')
