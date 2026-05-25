from django.db.models import Count
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from ingestion.tenant import get_tenant_from_request

from .models import NormalizedEmissionRecord, RecordStatus
from .serializers import (
    NormalizedEmissionRecordDetailSerializer,
    NormalizedEmissionRecordListSerializer,
)


class RecordViewSet(ReadOnlyModelViewSet):
    """GET /api/records/ and GET /api/records/{id}/ with filters."""

    def get_queryset(self):
        tenant = get_tenant_from_request(self.request)

        return (
            NormalizedEmissionRecord.objects
            .filter(tenant=tenant)
            .select_related('raw_record')
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NormalizedEmissionRecordDetailSerializer
        return NormalizedEmissionRecordListSerializer

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        record = self.get_object()
        record.status = RecordStatus.APPROVED
        record.reviewed_at = timezone.now()
        record.reviewed_by = request.data.get('reviewed_by', 'analyst')
        record.review_notes = request.data.get('notes', '')
        record.save()

        return Response(
            NormalizedEmissionRecordDetailSerializer(record).data
        )

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        record = self.get_object()

        record.status = RecordStatus.REJECTED
        record.reviewed_at = timezone.now()
        record.reviewed_by = request.data.get('reviewed_by', 'analyst')
        record.review_notes = request.data.get(
            'notes',
            request.data.get('reason', '')
        )

        record.save()

        return Response(
            NormalizedEmissionRecordDetailSerializer(record).data
        )


class DashboardView(APIView):
    """GET /api/dashboard/"""

    def get(self, request):
        try:
            tenant = get_tenant_from_request(request)

            qs = NormalizedEmissionRecord.objects.filter(
                tenant=tenant
            )

            total = qs.count()

            pending = qs.filter(status='PENDING').count()
            approved = qs.filter(status='APPROVED').count()
            rejected = qs.filter(status='REJECTED').count()

            return Response({
                "total": total,
                "pending": pending,
                "approved": approved,
                "rejected": rejected,
                "flagged": 0,
                "by_status": {},
                "by_source": {},
                "by_scope": {},
                "quality": {
                    "missing_fields": 0,
                    "invalid_units": 0,
                    "suspicious_values": 0,
                }
            })

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=500)