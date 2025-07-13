#!/usr/bin/python3

import json
from sys import argv

prefix = {0: "H/s", 1: "kH/s", 2: "MH/s", 3: "GH/s", 4: "TH/s"}

with open("hashcat_modes.json") as f:
    modes = json.load(f)

def mk_pretty(raw):
    i = 0
    while raw > 1000:
        i += 1
        raw = raw / 1000
    return f'{raw:.2f} {prefix[i]}'

def usage():
    print(f"\nUsage: {argv[0]} [-o comparison_output.json] hashcat_merged_1.json hashcat_merged_2.json\n")
    exit(0)

def mk_compare(a, b, common_keys, benchmarks):
    compare = {}
    for key in common_keys:
        c = a[key]['average']['raw']
        d = b[key]['average']['raw']
        if c != 0 and d != 0:
            compare[key] = {"name": modes[key]}
            if c > d:
                compare[key]['winner'] = benchmarks[0]
                compare[key]['diff'] = c/d - 1
                compare[key]['raw_diff'] = c - d
                compare[key]['pretty_winner'] = mk_pretty(c)
            else:
                compare[key]['winner'] = benchmarks[1]
                compare[key]['diff'] = d/c - 1
                compare[key]['raw_diff'] = d - c
                compare[key]['pretty_winner'] = mk_pretty(d)

            compare[key]['pretty_diff'] = mk_pretty(compare[key]['raw_diff'])
            compare[key]['percent'] = f"{(100*compare[key]['diff']):.2f}%"
    
    return compare

def main():
    if len(argv) < 3:
        usage()

    if argv[1] == '-o':
        outfile = argv[2]
        benchmarks = argv[3:]
    else:
        outfile = None
        benchmarks = argv[1:]

    if len(benchmarks) != 2:
        usage()

    with open(benchmarks[0]) as f:
        a = json.load(f)
    with open(benchmarks[1]) as f:
        b = json.load(f)
    
    a_keys = list(a.keys())
    b_keys = list(b.keys())
    common_keys = []
    for key in a_keys:
        if key in b_keys:
            common_keys.append(key)

    compare = mk_compare(a, b, common_keys, benchmarks)

    if outfile:
        with open(outfile, 'w') as f:
            json.dump(compare, f, indent=4)
    else:
        try:
            print(json.dumps(compare, indent=4))
        except BrokenPipeError:
            pass


if __name__ == '__main__':
    main()
