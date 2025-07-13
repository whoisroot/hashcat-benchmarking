#!/usr/bin/python3

import json
from os import popen
from re import search, sub, IGNORECASE


def get_help(flag):
    print("Running hashcat "+flag)
    hashcat_help = popen('hashcat '+flag).read().split('\n')
    for i in range(len(hashcat_help)):
        if search('Hash modes', hashcat_help[i], flags=IGNORECASE):
            i += 4
            break

    for j in range(i, len(hashcat_help)):
        if hashcat_help[j] == '':
            break

    return sorted(hashcat_help[i:j])

def extract_modes(help_output):
    hashmodes = {}
    for line in help_output:
        filtered = sub(r'^( +)([0-9]+ \| [^|]+)(.*)', r'\2', line).strip()
        data = filtered.split(' | ')
        hashmodes[data[0]] = data[1]
    return hashmodes

def main():
    help_output = get_help("--help")
    if len(help_output) < 10:
        print('Failed with "--help"')
        help_output = get_help("-hh")
    hashmodes = extract_modes(help_output)
    print(f"\nSaving {len(hashmodes)} known hash modes to hashcat_modes.json")
    with open("hashcat_modes.json", 'w') as f:
        json.dump(hashmodes, f, indent=4)

if __name__ == "__main__":
    main()
