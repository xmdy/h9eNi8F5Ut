import urlparse
from urllib import urlencode

import requests


def add_url_params(url, params):
    _parts = list(urlparse.urlparse(url))
    q = dict(urlparse.parse_qsl(_parts[4]))
    q.update(params)

    _parts[4] = urlencode(q)

    return urlparse.urlunparse(_parts)


def load_data_page(url, page=1, per_page=100):
    params = {'offset': (page-1)*per_page, 'limit': per_page}
    page_url = add_url_params(url, params)
    json_data = None
    try:
        req = requests.get(page_url)
        if req.status_code == 200:
            json_data = req.json()
    except Exception:
        pass  # ignore all exceptions
    return json_data


def load_source_data(url):
    data = []
    total = 1
    current_page = 1
    total_pages = 2
    while current_page < total_pages:
        page_data = load_data_page()