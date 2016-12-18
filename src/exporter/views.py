import datetime
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from exporter.models import ModelExport
from exporter.serializers import ModelExportSerializer


class ExportViewSet(viewsets.ModelViewSet):
    serializer_class = ModelExportSerializer
    queryset = ModelExport.objects.all()

    def perform_destroy(self, instance):
        raise ValidationError('You can\'t remove any objects')

    def filter_queryset___(self, queryset):
        user_id = self.request.GET.get('user_id')

        created__gte = self.request.GET.get('created__gte')
        created__lte = self.request.GET.get('created__lte')

        if user_id:
            queryset = queryset \
                .filter(user_id=user_id)

        if created__gte:
            try:
                datetime.datetime.strptime(created__gte, '%Y-%m-%d')
            except ValueError:
                raise ValidationError("Created__gte incorrect data format, should be YYYY-MM-DD")

            queryset = queryset.filter(created__gte=created__gte)

        if created__lte:
            try:
                datetime.datetime.strptime(created__lte, '%Y-%m-%d')
            except ValueError:
                raise ValidationError("Created__lte incorrect data format, should be YYYY-MM-DD")

            queryset = queryset.filter(created__lte=created__lte)

        return queryset
