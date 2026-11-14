import copy
import tempfile
import unittest
from bindings import read_path
from flow import SAMPLE, validate, fingerprint
from local_http import serve
from fixture_sources import Sources
from handlers import Collectors
from static_runner import execute_static


class FlowTests(unittest.TestCase):
    def test_static_chain_consumes_real_source(self):
        source = Sources()
        with tempfile.TemporaryDirectory() as directory, serve(source) as base:
            result = execute_static(SAMPLE, Collectors(base), directory)
            self.assertEqual(result['steps']['summary']['state'], 'done')
            self.assertEqual(result['outputs']['summary']['records'][0]['id'], 'record-1')
            self.assertEqual(len(source.calls), 3)

    def test_failed_source_does_not_run_summary(self):
        source = Sources()
        source.fail.add('/details')
        with tempfile.TemporaryDirectory() as directory, serve(source) as base:
            result = execute_static(SAMPLE, Collectors(base), directory)
            self.assertEqual(result['steps']['detail']['state'], 'failed')
            self.assertNotIn('summary', result['steps'])

    def test_binding_and_configuration_identity(self):
        self.assertEqual(read_path({'items': [{'id': 'one'}]}, 'items.0.id'), 'one')
        altered = copy.deepcopy(SAMPLE)
        altered['revision'] += 1
        self.assertNotEqual(fingerprint(SAMPLE), fingerprint(altered))

    def test_invalid_dependency_is_not_dispatched(self):
        altered = copy.deepcopy(SAMPLE)
        altered['steps'].reverse()
        with self.assertRaises(ValueError):
            validate(altered)
