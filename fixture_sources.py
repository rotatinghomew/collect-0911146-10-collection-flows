from urllib.parse import urlsplit, parse_qs
from local_http import Reply


class Sources:
    def __init__(self):
        self.calls = []
        self.fail = set()

    def handle(self, method, path, headers, body):
        parsed = urlsplit(path)
        query = {name: values[0] for name, values in parse_qs(parsed.query).items()}
        self.calls.append((parsed.path, query))
        if parsed.path in self.fail:
            return Reply.json({'error': 'source unavailable'}, 503)
        if parsed.path == '/institutions':
            return Reply.json({'items': [{'id': 'inst-a'}, {'id': 'inst-b'}]})
        if parsed.path == '/directories':
            institution = query.get('institution')
            if institution == 'inst-a':
                return Reply.json({'items': [{'id': 'dir-1'}, {'id': 'dir-2'}]})
            if institution == 'inst-b':
                return Reply.json({'items': []})
            return Reply(404)
        if parsed.path == '/details':
            directory = query.get('directory')
            if directory == 'dir-1':
                return Reply.json({'items': [{'id': 'record-1', 'attachments': ['att-1']}]})
            if directory == 'dir-2':
                return Reply.json({'items': [{'id': 'record-2', 'attachments': []}]})
            return Reply(404)
        if parsed.path == '/attachment_meta':
            if query.get('attachment') == 'att-1':
                return Reply.json({'id': 'att-1', 'bytes': 512, 'media_type': 'application/pdf'})
            return Reply(404)
        return Reply(404)
