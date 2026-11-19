#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nativetap search — local search over mobile UI/UX data.
Usage: python search.py "<query>" [--domain <domain>] [--max-results 3]
Domains: styles, gestures, safe-areas, flutter, swiftui, kotlin, hig-ios,
         material3, typography, color, motion, icons
"""
import argparse
import csv
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, '..', 'data')

DOMAINS = {
    'styles': 'styles.csv',
    'gestures': 'gestures.csv',
    'safe-areas': 'safe-areas.csv',
    'flutter': 'flutter-patterns.csv',
    'swiftui': 'swiftui-patterns.csv',
    'kotlin': 'kotlin-patterns.csv',
    'hig-ios': 'hig-ios.csv',
    'material3': 'material3.csv',
    'typography': 'typography-mobile.csv',
    'color': 'color-mobile.csv',
    'motion': 'motion.csv',
    'icons': 'app-icons.csv',
}

TITLE_KEYS = ('problem', 'interaction', 'topic', 'gesture', 'component',
              'style', 'area', 'role', 'asset')

WEIGHTED_KEYS = TITLE_KEYS


def load_rows(domain):
    path = os.path.join(DATA, DOMAINS[domain])
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def score_row(query_terms, row):
    """Token-overlap scoring with field weighting."""
    score = 0
    for key, value in row.items():
        if not value:
            continue
        v = value.lower()
        weight = 3 if key in WEIGHTED_KEYS else 1
        for term in query_terms:
            if term in v:
                score += weight
    return score


def title_of(row):
    for key in TITLE_KEYS:
        if row.get(key):
            return row[key]
    return 'row'


def format_row(domain, row):
    lines = [f"### {domain}: {title_of(row)}"]
    for key, value in row.items():
        if value:
            lines.append(f"- **{key}:** {value}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='nativetap search')
    parser.add_argument('query', nargs='?', default=None)
    parser.add_argument('--domain', default=None)
    parser.add_argument('--max-results', type=int, default=3)
    parser.add_argument('--list-domains', action='store_true')
    args = parser.parse_args()

    if args.list_domains:
        print('Available domains:')
        for d in DOMAINS:
            print(' ', d)
        return

    if not args.query:
        print('Usage: python search.py "<query>" [--domain <domain>]')
        return

    domains = [args.domain] if args.domain else list(DOMAINS)
    if args.domain and args.domain not in DOMAINS:
        print(f"Unknown domain '{args.domain}'. Available: {', '.join(DOMAINS)}")
        sys.exit(1)

    terms = [t for t in args.query.lower().split() if len(t) > 1]
    results = []
    for domain in domains:
        for row in load_rows(domain):
            s = score_row(terms, row)
            if s > 0:
                results.append((s, domain, row))

    results.sort(key=lambda x: -x[0])
    if not results:
        print(f"No matches for '{args.query}'. Try --list-domains.")
        return

    for s, domain, row in results[: args.max_results]:
        print(format_row(domain, row))
        print()


if __name__ == '__main__':
    main()
