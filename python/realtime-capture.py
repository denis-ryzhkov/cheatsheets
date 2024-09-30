#!/usr/bin/env python3
import selectors
import subprocess
import sys
from typing import IO, Dict, cast

sub = subprocess.Popen(
    ["bash", "-c", "for i in $(seq 5); do echo out $i && echo err $i >&2; done"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

assert sub.stdout and sub.stderr
lines = []

streams: Dict[IO[str], IO[str]] = {
    sub.stdout: sys.stdout,
    sub.stderr: sys.stderr,
}

with selectors.DefaultSelector() as selector:
    for sub_stream, sys_stream in streams.items():
        selector.register(sub_stream, selectors.EVENT_READ, sys_stream)

    while streams:
        for selected, _ in selector.select():
            sub_stream = cast(IO[str], selected.fileobj)
            if sub_stream not in streams:
                continue

            line = sub_stream.readline()
            if not line:
                streams.pop(sub_stream)
                continue

            sys_stream = selected.data
            sys_stream.write(line)
            sys_stream.flush()

            lines.append(line)

exit_code = sub.wait()
print(exit_code, len(lines))
