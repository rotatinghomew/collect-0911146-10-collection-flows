import hashlib
import json


SAMPLE = {'name': 'single-directory', 'revision': 1, 'steps': [
    {'id': 'institutions', 'kind': 'institutions', 'arguments': {}},
    {'id': 'directory', 'kind': 'directories', 'arguments': {'institution': {'from': 'institutions', 'path': 'items.0.id'}}},
    {'id': 'detail', 'kind': 'details', 'arguments': {'directory': {'from': 'directory', 'path': 'items.0.id'}}},
    {'id': 'summary', 'kind': 'summary', 'arguments': {'records': {'from': 'detail', 'path': 'items'}}},
]}


def validate(flow):
    identities = [step['id'] for step in flow['steps']]
    if not identities or len(identities) != len(set(identities)):
        raise ValueError('步骤标识为空或重复')
    available = set()
    for step in flow['steps']:
        for value in step.get('arguments', {}).values():
            if isinstance(value, dict) and 'from' in value and value['from'] not in available:
                raise ValueError('静态流程的输入尚未产生')
        available.add(step['id'])
    return flow


def fingerprint(flow):
    return hashlib.sha256(json.dumps(flow, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
