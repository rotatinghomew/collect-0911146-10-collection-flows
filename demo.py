import json
import tempfile
from local_http import serve
from fixture_sources import Sources
from flow import SAMPLE
from handlers import Collectors
from static_runner import execute_static


def main():
    with tempfile.TemporaryDirectory() as directory, serve(Sources()) as base:
        print(json.dumps(execute_static(SAMPLE, Collectors(base), directory), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
