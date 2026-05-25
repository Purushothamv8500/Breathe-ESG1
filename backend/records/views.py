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

        pending = by_status.get('PENDING', 0)
        approved = by_status.get('APPROVED', 0)
        rejected = by_status.get('REJECTED', 0)

        missing_fields = 0
        invalid_units = 0
        suspicious_values = 0
        flagged = 0

        for flags in qs.values_list('quality_flags', flat=True):
            if not flags:
                continue

            flagged += 1

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