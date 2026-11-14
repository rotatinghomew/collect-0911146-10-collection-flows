from bindings import resolve
from evidence import EvidenceStore
from flow import validate, fingerprint
from runs import run_view


def execute_static(flow, collectors, directory):
    validate(flow)
    store = EvidenceStore(directory)
    outputs = {}
    version = fingerprint(flow)
    for step in flow['steps']:
        store.record({'step': step['id'], 'state': 'running', 'flow': version})
        try:
            arguments = resolve(step.get('arguments', {}), outputs)
            result = collectors.call(step['kind'], arguments)
        except (ValueError, KeyError, IndexError) as error:
            store.record({'step': step['id'], 'state': 'failed', 'flow': version, 'error': str(error)})
            break
        outputs[step['id']] = result
        store.record({'step': step['id'], 'state': 'done', 'flow': version, 'result': result})
    return {'flow': version, 'outputs': outputs, 'steps': run_view(store.events())}
