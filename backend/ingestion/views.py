from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from records.models import SourceType

from .parsers import parse_upload
from .service import ingest_rows
from .tenant import get_tenant_from_request


class BaseIngestView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    source_type = None

    def post(self, request):
        tenant = get_tenant_from_request(request)

        if request.FILES.get('file'):
            uploaded = request.FILES['file']
            rows = parse_upload(uploaded, uploaded.content_type)
            filename = uploaded.name
            content_type = uploaded.content_type
        elif isinstance(request.data, list):
            rows = request.data
            filename = 'json_body'
            content_type = 'application/json'
        elif isinstance(request.data, dict) and 'rows' in request.data:
            rows = request.data['rows']
            filename = 'json_body'
            content_type = 'application/json'
        else:
            return Response(
                {'error': 'Provide CSV file as "file" or JSON array/{"rows": [...]}'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not rows:
            return Response({'error': 'No data rows found'}, status=status.HTTP_400_BAD_REQUEST)

        result = ingest_rows(tenant, self.source_type, rows, filename, content_type)
        return Response(result, status=status.HTTP_201_CREATED)


class IngestSAPView(BaseIngestView):
    source_type = SourceType.SAP


class IngestUtilityView(BaseIngestView):
    source_type = SourceType.UTILITY


class IngestTravelView(BaseIngestView):
    source_type = SourceType.TRAVEL
