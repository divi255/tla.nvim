#!/usr/bin/env python3

import subprocess
import sys
import select
from neotermcolor import cprint

sys.argv.pop(0)

# Start the subprocess and get stdout, stderr
process = subprocess.Popen(sys.argv,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           text=True)

while True:
    reads = [process.stdout.fileno(), process.stderr.fileno()]
    ret = select.select(reads, [], [])
    line = None

    for fd in ret[0]:
        if fd == process.stdout.fileno():
            line = process.stdout.readline().strip()
        if fd == process.stderr.fileno():
            line = process.stderr.readline().strip()

    if line is not None:
        if 'No error has been found' in line:
            cprint(line, 'green')
        elif line.startswith('Error:'):
            cprint(line, 'red')
        else:
            print(line)

    if process.poll() is not None:
        break
