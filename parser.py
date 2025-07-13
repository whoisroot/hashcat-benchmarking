#!/usr/bin/python3

import json
from sys import argv
from re import search

prefix = {0: "H/s", 1: "kH/s", 2: "MH/s", 3: "GH/s", 4: "TH/s"}

def mk_pretty(raw):
    i = 0
    while raw > 1000:
        i += 1
        raw = raw / 1000
    return f'{raw:.2f} {prefix[i]}'

def main():
    if len(argv) < 2:
        print(f"\nUsage: {argv[0]} hashcat_benchmark.txt [output.json]\n")
        exit(0)

    with open("hashcat_modes.json") as f:
        modes = json.load(f)

    with open(argv[1]) as f:
        raw_results = f.read().strip('\n').split('\n')

    for i in range(len(raw_results)):
        if search(r'^[0-9.:]+$', raw_results[i]):
            break
    raw_results = raw_results[i:]

    benchmark = {}
    for result in raw_results:
        data = result.split(':')
        if len(data) != 6:
            continue
        device, mode, _, _, _, raw = data
        if mode not in benchmark.keys():
            name = modes[mode]
            benchmark[mode] = {"name": name, "devices": {}, "total": {"pretty": "", "raw": 0}}
        raw = float(raw)
        pretty = mk_pretty(raw)
        benchmark[mode]["devices"][device] = {"pretty": pretty, "raw": raw}
        benchmark[mode]["total"]["raw"] += raw
        benchmark[mode]["total"]["pretty"] = mk_pretty(benchmark[mode]["total"]["raw"])


    if len(argv) == 3:
        with open(argv[2], 'w') as f:
            json.dump(benchmark, f, indent=4)
    else:
        try:
            print(json.dumps(benchmark, indent=4))
        except BrokenPipeError:
            pass

if __name__ == '__main__':
    main()
