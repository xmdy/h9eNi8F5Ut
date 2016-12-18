import json
import dicttoxml
from cStringIO import StringIO


class RenderException(Exception):
    pass


class DataRender(object):
    _format_slug = None
    _file_ext = None

    def __init__(self, data=None):
        self.data = data

    def set_data(self, data):
        self.data = data

    def render(self):
        raise NotImplementedError('Renderer must implement render method')

    def file_obj(self):
        return StringIO(self.render())

    @classmethod
    def format_slug(cls):
        return cls._format_slug

    @classmethod
    def file_ext(cls):
        return cls._file_ext


class XmlDataRender(DataRender):
    _format_slug = 'xml'
    _file_ext = 'xml'

    def render(self):
        return dicttoxml.dicttoxml(self.data)


class JsonDataRenderer(DataRender):
    _format_slug = 'json'
    _file_ext = 'json'

    def render(self):
        return json.dumps(self.data)


class XmlZipDataRender(XmlDataRender):
    _format_slug = 'xml_zip'
    _file_ext = 'xml.zip'

    def render(self):
        data = super(XmlZipDataRender, self).render()
        from zipfile import ZipFile

        inmemory_file = StringIO()

        zip_file_obj = ZipFile(inmemory_file, 'w')
        zip_file_obj.writestr('data.xml', data)
        zip_file_obj.close()

        inmemory_file.seek(0)

        return inmemory_file.read()


class RenderManager(object):
    renders = {}

    def register_renderer(self, render):
        """
        Register render format
        :type render: DataRender
        """
        self.renders[render.format_slug()] = render

    def get_render(self, format_slug):
        """
        Get render for format slug
        :type format_slug: str
        :raise RenderException
        :return DataRender
        """
        if format_slug in self.renders:
            return self.renders[format_slug]

        raise RenderException('unknown render format')

    def render(self, format_slug, data):
        data_render_cls = self.get_render(format_slug)

        data_render = data_render_cls(data)

        return data_render.render()

    def file_ext(self, format_slug):
        return self.get_render(format_slug).file_ext()

    def render_to_file_obj(self, format_slug, data):
        data_render_cls = self.get_render(format_slug)

        data_render = data_render_cls(data)

        return data_render.file_obj()

    def get_registered_renders(self):
        return [(el, el) for el in self.renders.keys()]


render_manager = RenderManager()

render_manager.register_renderer(XmlDataRender)
render_manager.register_renderer(XmlZipDataRender)
render_manager.register_renderer(JsonDataRenderer)
