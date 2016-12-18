from __future__ import absolute_import, unicode_literals
import json
import urlparse

import math

from application.celery import app
from celery import shared_task

from django.core.files.base import ContentFile
from django.utils.functional import cached_property

from application import settings
from exporter.helpers import load_data_page, add_url_params
from exporter.models import ModelExport
from exporter.renderers import render_manager

data_source_url = getattr(settings, 'EXPORTER_DATA_SOURCE_URL', 'http://localhost:8000/comments/')


class GenerateModelExportTask(app.Task):
    ignore_result = True
    data = None
    modelexport_id = None

    def run(self, modelexport_id, per_page=100, *args, **kwargs):
        self.modelexport_id = modelexport_id
        self.per_page = per_page
        self.data = []

        if not self.export_obj:
            return

        self.lock_export()

        self.generate_data_file()
        self.generate_formatted_file()

        self.finish_export()

    @cached_property
    def export_obj(self):
        try:
            return ModelExport.objects.get(id=self.modelexport_id, status='new')
        except ModelExport.DoesNotExist:
            return ModelExport.objects.none()

    @cached_property
    def source_url(self):
        created_at = self.export_obj.created_at

        url = data_source_url
        conditions = dict(urlparse.parse_qsl(self.export_obj.conditions))
        conditions['created_at__lte'] = '%s-%s-%s' % (created_at.year, created_at.month, created_at.day)  # export only objects created before export moment
        return add_url_params(url, conditions)

    def load_source_data(self):
        current_page = 1
        total_pages = 1  # assume we have data

        while current_page <= total_pages:
            page_data = load_data_page(self.source_url, page=current_page, per_page=self.per_page)

            if not page_data:
                break

            if current_page == 1:
                total_pages = math.ceil(page_data.get('count')/float(self.per_page))

            self.data.extend(page_data.get('results', []))
            current_page += 1

    def generate_data_file(self):
        if self.export_obj.export_data:
            return

        self.load_source_data()

        cf = ContentFile(json.dumps(self.data))
        name = 'export_data_%s.json' % self.modelexport_id

        self.export_obj.export_data.save(name, cf)

    def generate_formatted_file(self):
        if self.export_obj.export_file:
            return

        export_data = json.loads(self.export_obj.export_data.read())
        buf_obj = render_manager.render(self.export_obj.export_format, export_data)
        cf = ContentFile(buf_obj)

        file_ext = render_manager.file_ext(self.export_obj.export_format)
        name = 'export_%s.%s' % (self.modelexport_id, file_ext)

        self.export_obj.export_file.save(name, cf)

    def lock_export(self):
        self.export_obj.set_status('processing')

    def finish_export(self):
        self.export_obj.set_status('success')
