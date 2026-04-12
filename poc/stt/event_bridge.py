#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import urllib.request
from typing import Any


def post_event(server_url: str, payload: dict[str, Any]) -> dict[str, Any]:
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        server_url.rstrip('/') + '/ingest',
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    with urllib.request.urlopen(req) as response:
        body = response.read().decode('utf-8')
    return json.loads(body)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', default='http://127.0.0.1:8788')
    parser.add_argument('--event', required=True, help='Raw JSON payload')
    args = parser.parse_args()
    payload = json.loads(args.event)
    print(json.dumps(post_event(args.server, payload), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
