from pathlib import Path
import hashlib
import json
import os
import re
import tempfile


class EvidenceStore:
    def __init__(self, root):
        self.root = Path(root)
        self.blobs = self.root / 'blobs'
        self.blobs.mkdir(parents=True, exist_ok=True)

    def put(self, body):
        if not isinstance(body, bytes):
            raise TypeError('证据必须是字节')
        digest = hashlib.sha256(body).hexdigest()
        destination = self.blobs / digest
        descriptor, temporary = tempfile.mkstemp(dir=self.blobs)
        try:
            with os.fdopen(descriptor, 'wb') as stream:
                stream.write(body)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, destination)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        return digest

    def get(self, digest):
        if not re.fullmatch('[0-9a-f]{64}', digest):
            raise ValueError('非法证据标识')
        body = (self.blobs / digest).read_bytes()
        if hashlib.sha256(body).hexdigest() != digest:
            raise ValueError('证据摘要不匹配')
        return body

    def record(self, event):
        line = json.dumps(event, ensure_ascii=False, sort_keys=True) + '\n'
        with (self.root / 'events.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(line)
            stream.flush()
            os.fsync(stream.fileno())

    def events(self):
        path = self.root / 'events.jsonl'
        if not path.exists():
            return []
        return [json.loads(line) for line in path.read_text().splitlines()]
