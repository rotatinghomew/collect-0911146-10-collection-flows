def read_path(value, path):
    current = value
    for part in path.split('.') if path else []:
        if isinstance(current, list) and part.isdigit():
            current = current[int(part)]
        elif isinstance(current, dict):
            current = current[part]
        else:
            raise ValueError('无法读取绑定路径：' + path)
    return current


def resolve(arguments, outputs):
    result = {}
    for name, value in arguments.items():
        if isinstance(value, dict) and 'from' in value:
            result[name] = read_path(outputs[value['from']], value.get('path', ''))
        else:
            result[name] = value
    return result
