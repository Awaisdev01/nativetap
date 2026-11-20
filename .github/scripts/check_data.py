#!/usr/bin/env python3
"""Data integrity check: every CSV parses, every row has all columns."""
import csv
import glob
import os
import sys

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    '..', '..', '.claude', 'skills', 'nativetap', 'data')
failures = []
for path in sorted(glob.glob(os.path.join(DATA, '*.csv'))):
    name = os.path.basename(path)
    with open(path, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    if not rows:
        failures.append(f"{name}: no rows")
        continue
    expected = set(rows[0].keys())
    if None in expected:
        failures.append(f"{name}: header/column count mismatch")
        continue
    for i, row in enumerate(rows, 2):
        if set(row.keys()) != expected:
            failures.append(f"{name}: line {i} column mismatch")
        if all((v or '').strip() == '' for v in row.values()):
            failures.append(f"{name}: line {i} fully empty")

if failures:
    print('\n'.join(failures))
    sys.exit(1)
print('OK: all CSVs parse cleanly')
