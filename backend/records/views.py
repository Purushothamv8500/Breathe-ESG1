from django.db.models import Count
from django.utils import timezone
from rest_framework import status
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
        qs = NormalizedEmissionRecord.objects.filter(tenant=tenant).select_related('raw_record')

        source = self.request.query_params.get('source')
        if source:
            qs = qs.filter(source_type=source.upper())

        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter.upper())

        scope = self.request.query_params.get('scope')
        if scope:
            qs = qs.filter(scope=scope.upper())

        return qs

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
        return Response(NormalizedEmissionRecordDetailSerializer(record).data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        record = self.get_object()
        record.status = RecordStatus.REJECTED
        record.reviewed_at = timezone.now()
        record.reviewed_by = request.data.get('reviewed_by', 'analyst')
        record.review_notes = request.data.get('notes', request.data.get('reason', ''))
        record.save()
        return Response(NormalizedEmissionRecordDetailSerializer(record).data)


class DashboardView(APIView):
    """GET /api/dashboard/ — summary stats for analyst home."""

    def get(self, request):
        tenant = get_tenant_from_request(request)
        qs = NormalizedEmissionRecord.objects.filter(tenant=tenant)

        by_status = dict(
            qs.values('status').annotate(count=Count('id')).values_list('status', 'count')
        )
        by_source = dict(
            qs.values('source_type').annotate(count=Count('id')).values_list('source_type', 'count')
        )
        by_scope = dict(
            qs.values('scope').annotate(count=Count('id')).values_list('scope', 'count')
        )

        flagged = qs.exclude(quality_flags=[]).count()
        pending = by_status.get('PENDING', 0)
        approved = by_status.get('APPROVED', 0)
        rejected = by_status.get('REJECTED', 0)

        missing_fields = 0
        invalid_units = 0
        suspicious_values = 0
        for flags in qs.values_list('quality_flags', flat=True):
            if not flags:
                continue
            if 'MISSING_FIELD' in flags:
                missing_fields += 1
            if 'INVALID_UNIT' in flags:
                invalid_units += 1
            if 'SUSPICIOUS_VALUE' in flags:
                suspicious_values += 1

        return Response({
            'total': qs.count(),
            'pending': pending,
            'approved': approved,
            'rejected': rejected,
            'flagged': flagged,
            'by_status': by_status,
            'by_source': by_source,
            'by_scope': by_scope,
            'quality': {
                'missing_fields': missing_fields,
                'invalid_units': invalid_units,
                'suspicious_values': suspicious_values,
            },
        })
