def run_view(events):
    by_step = {}
    for event in events:
        by_step[event['step']] = {'state': event['state'], 'result': event.get('result'), 'error': event.get('error')}
    return by_step
