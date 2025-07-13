#!/usr/bin/python3

import json
from sys import argv

prefix = {0: "H/s", 1: "kH/s", 2: "MH/s", 3: "GH/s", 4: "TH/s"}

def mk_pretty(raw):
    i = 0
    while raw > 1000:
        i += 1
        raw = raw / 1000
    return f'{raw:.2f} {prefix[i]}'

if len(argv) < 3 or (len(argv) < 4 and argv[1] == "-o"):
    print(f"\nUsage: {argv[0]} [-o output_file.json] benchmark1.json benchmark2.json [...]\n")
    exit(0)

if argv[1] == '-o':
    outfile = argv[2]
    benchmarks = argv[3:]
else:
    outfile = None
    benchmarks = argv[1:]

merged = {}

for bench in benchmarks:
    with open(bench) as f:
        results = json.load(f)
    for hashtype in results.keys():
        if hashtype not in merged.keys():
            merged[hashtype] = {'name': results[hashtype]['name'], "raws": [], "pretties": []}
        merged[hashtype]['raws'].append(results[hashtype]['total']['raw'])
        merged[hashtype]['pretties'].append(results[hashtype]['total']['pretty'])

for hashtype in merged.keys():
    total = 0
    for raw in merged[hashtype]['raws']:
        total += raw
    raw_average = total/len(merged[hashtype]['raws'])
    merged[hashtype]['average'] = {"pretty": mk_pretty(raw_average), "raw": raw_average}

if outfile != None:
    with open(outfile, "w") as f:
        json.dump(merged, f, indent=4)
else:
    print(json.dumps(merged, indent=4))
