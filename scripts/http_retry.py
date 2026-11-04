#!/usr/bin/env python3
"""Bounded, fail-closed HTTP retrieval for astronomy catalog importers.

Retries only network failures and transient HTTP status codes. Callers must
still validate schema, source identity, coordinates, units and row counts
before modifying their last-known-good curated datasets.
"""
import time
import urllib.error
import urllib.request

TRANSIENT_HTTP = frozenset({408, 429, 500, 502, 503, 504})


def read_bounded(request, *, max_bytes, timeout, attempts=3, backoff_seconds=2, opener=None, sleeper=None):
    """Fetch at most max_bytes bytes; raise on oversized data or exhausted retries.

    Network retries are limited, so a provider outage cannot turn into an
    unbounded polling loop. Never accepts an HTTP error response as data.
    """
    if max_bytes <= 0 or timeout <= 0 or not 1 <= attempts <= 5:
        raise ValueError("Invalid bounded-fetch configuration")
    opener = opener or urllib.request.urlopen
    sleeper = sleeper or time.sleep
    for attempt in range(attempts):
        try:
            with opener(request, timeout=timeout) as response:
                status = response.status
                if status != 200:
                    raise urllib.error.HTTPError(
                        request.full_url if hasattr(request, "full_url") else str(request),
                        status, "Unexpected status", response.headers, None
                    )
                payload = response.read(max_bytes + 1)
                if len(payload) > max_bytes:
                    raise ValueError("Catalog response exceeds configured byte cap")
                return payload
        except urllib.error.HTTPError as exc:
            if exc.code not in TRANSIENT_HTTP or attempt + 1 >= attempts:
                raise
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
            if attempt + 1 >= attempts:
                raise
        sleeper(backoff_seconds * (2 ** attempt))
    raise AssertionError("unreachable")


def self_test():
    from io import BytesIO

    class Response:
        status = 200
        headers = {}
        def __init__(self, data):
            self.body = BytesIO(data)
        def __enter__(self):
            return self
        def __exit__(self, *args):
            self.body.close()
        def read(self, n):
            return self.body.read(n)

    calls = []
    def flaky(req, timeout):
        calls.append(timeout)
        if len(calls) < 3:
            raise urllib.error.URLError("transient")
        return Response(b"source-data")
    assert read_bounded("unused", max_bytes=64, timeout=5, opener=flaky, sleeper=lambda n: None) == b"source-data"
    assert len(calls) == 3
    try:
        read_bounded("unused", max_bytes=3, timeout=5,
                     opener=lambda req, timeout: Response(b"too-large"), sleeper=lambda n: None)
        raise AssertionError("oversized response accepted")
    except ValueError:
        pass

    fail_calls = []
    def always_down(req, timeout):
        fail_calls.append(timeout)
        raise urllib.error.HTTPError("url", 502, "Bad Gateway", {}, None)
    try:
        read_bounded("unused", max_bytes=64, timeout=5, attempts=2,
                     opener=always_down, sleeper=lambda n: None)
        raise AssertionError("transient failure accepted")
    except urllib.error.HTTPError as exc:
        assert exc.code == 502
    assert len(fail_calls) == 2
    print("Bounded HTTP retry self-test passed")


if __name__ == "__main__":
    self_test()
