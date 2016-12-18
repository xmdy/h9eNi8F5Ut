from __future__ import absolute_import
from rest_framework import serializers

from exporter.models import ModelExport
from exporter.renderers import render_manager
from .tasks import GenerateModelExportTask


class ModelExportSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=True)

    created_at = serializers.DateTimeField(allow_null=True)
    updated_at = serializers.DateTimeField(allow_null=True)

    user_id = serializers.CharField(max_length=36)

    conditions = serializers.CharField()

    export_file = serializers.FileField(allow_null=True)
    export_format = serializers.ChoiceField(choices=render_manager.get_registered_renders())

    status = serializers.CharField()

    def create(self, validated_data):
        obj = ModelExport.objects.create(**validated_data)
        gmet = GenerateModelExportTask()
        # gmet.apply_async([obj.id])  # uncomment for production use
        gmet.run(obj.id)
        return obj

    def update(self, instance, validated_data):
        # update didn't allowed
        return instance
