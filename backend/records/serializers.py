from rest_framework import serializers

from .models import NormalizedEmissionRecord, RawDataRecord


class RawDataRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawDataRecord
        fields = ('id', 'source_type', 'payload', 'filename', 'checksum', 'ingested_at')


class NormalizedEmissionRecordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormalizedEmissionRecord
        fields = (
            'id', 'source_type', 'status', 'scope', 'activity_date', 'category',
            'description', 'location', 'quantity_normalized', 'unit_normalized',
            'quality_flags', 'created_at', 'reviewed_at', 'reviewed_by',
        )


class NormalizedEmissionRecordDetailSerializer(serializers.ModelSerializer):
    raw_record = RawDataRecordSerializer(read_only=True)
    raw_row = serializers.SerializerMethodField()

    class Meta:
        model = NormalizedEmissionRecord
        fields = (
            'id', 'source_type', 'status', 'scope', 'activity_date', 'category',
            'description', 'location', 'quantity_raw', 'unit_raw',
            'quantity_normalized', 'unit_normalized', 'emission_factor', 'co2e_kg',
            'quality_flags', 'normalized_payload', 'raw_record', 'raw_row',
            'source_row_index', 'created_at', 'updated_at', 'reviewed_at',
            'reviewed_by', 'review_notes', 'edited_flag',
        )

    def get_raw_row(self, obj):
        payload = obj.raw_record.payload or {}
        rows = payload.get('rows', [])
        idx = obj.source_row_index
        if idx < len(rows):
            return rows[idx]
        return None
