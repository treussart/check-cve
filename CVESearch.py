#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

from urllib.parse import urljoin


class CVESearch(object):

    def __init__(self, base_url='https://cve.circl.lu', proxies=None):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.proxies = proxies
        self.session.headers.update({
            'content-type': 'application/json',
            'User-Agent': 'PyCVESearch - python wrapper'})

    def _http_get(self, api_call, query=None):
        if query is None:
            response = self.session.get(urljoin(self.base_url, 'api/{}'.format(api_call)))
        else:
            response = self.session.get(urljoin(self.base_url, 'api/{}/{}'.format(api_call, query)))
        return response

    def cvefor(self, param):
        """ cvefor() returns a dict containing the CVE's for a given CPE ID
        """
        data = self._http_get('cvefor', query=param)
        return data.json()
