import json
from urllib.parse import urlencode
from local_http import request


class Collectors:
    def __init__(self, base):
        self.base = base

    def call(self, kind, arguments):
        if kind not in {'institutions', 'directories', 'details', 'attachment_meta', 'summary'}:
            raise ValueError('未知采集步骤')
        if kind == 'summary':
            return {'records': arguments['records']}
        url = self.base + '/' + kind
        if arguments:
            url += '?' + urlencode(arguments)
        reply = request(url)
        if reply.status != 200:
            raise ValueError('步骤来源失败：' + kind + ':' + str(reply.status))
        return json.loads(reply.body)
