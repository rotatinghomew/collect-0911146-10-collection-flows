import tempfile
import unittest
from pathlib import Path
from evidence import EvidenceStore


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.store = EvidenceStore(self.temporary.name)

    def test_bytes_survive_new_instance(self):
        digest = self.store.put('原文\r\n'.encode())
        self.assertEqual(EvidenceStore(self.temporary.name).get(digest), '原文\r\n'.encode())

    def test_content_identity_and_journal_order(self):
        first = self.store.put(b'one')
        self.assertEqual(first, self.store.put(b'one'))
        self.assertNotEqual(first, self.store.put(b'two'))
        self.store.record({'kind': 'one', 'blob': first})
        self.store.record({'kind': 'two'})
        self.assertEqual([event['kind'] for event in self.store.events()], ['one', 'two'])

    def test_invalid_digest_and_corruption(self):
        with self.assertRaises(ValueError):
            self.store.get('../outside')
        digest = self.store.put(b'valid')
        (Path(self.temporary.name) / 'blobs' / digest).write_bytes(b'damaged')
        with self.assertRaises(ValueError):
            self.store.get(digest)
