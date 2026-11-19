#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nativetap search — local search over mobile UI/UX data.

Usage:
  python search.py "<query>" [--domain <d>] [--max-results 3] [--json]
  python search.py --list-domains
  python search.py --checklist            # 40 thumb rules P0-P5
  python search.py --stats
  python search.py "<query>" --stack flutter   # auto-route to relevant domains

Domains (23): styles, gestures, safe-areas, flutter, swiftui, kotlin, hig-ios,
  material3, typography, color, motion, icons, a11y, performance, forms,
  components, notifications, tablet-foldable, store, navigation, offline,
  onboarding, monetization
"""
import argparse
import csv
import json
import os
import re
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
    'a11y': 'a11y.csv',
    'performance': 'performance.csv',
    'forms': 'forms.csv',
    'components': 'components-specs.csv',
    'notifications': 'notifications.csv',
    'tablet-foldable': 'tablet-foldable.csv',
    'store': 'assets-store.csv',
    'navigation': 'navigation-ia.csv',
    'offline': 'networking-offline.csv',
    'onboarding': 'onboarding-retention.csv',
    'monetization': 'monetization.csv',
}

# Stack routing: query --stack <s> restricts to the domains that matter for
# that stack plus the universal ones.
STACK_DOMAINS = {
    'flutter': ['flutter', 'hig-ios', 'material3', 'gestures', 'safe-areas',
                'typography', 'color', 'motion', 'a11y', 'performance',
                'forms', 'components', 'navigation', 'offline', 'icons'],
    'swiftui': ['swiftui', 'hig-ios', 'gestures', 'safe-areas', 'typography',
                'color', 'motion', 'a11y', 'performance', 'forms',
                'components', 'navigation', 'offline', 'icons'],
    'kotlin': ['kotlin', 'material3', 'gestures', 'safe-areas', 'typography',
               'color', 'motion', 'a11y', 'performance', 'forms',
               'components', 'navigation', 'offline', 'icons'],
    'design': ['styles', 'gestures', 'hig-ios', 'material3', 'typography',
               'color', 'motion', 'components', 'navigation', 'onboarding'],
    'launch': ['icons', 'store', 'notifications', 'monetization',
               'performance', 'onboarding'],
}

TITLE_KEYS = ('problem', 'interaction', 'topic', 'gesture', 'component',
              'style', 'area', 'role', 'asset', 'pattern')

STOPWORDS = {'the', 'a', 'an', 'is', 'are', 'to', 'of', 'in', 'on', 'for',
             'and', 'or', 'it', 'be', 'do', 'how', 'what', 'when', 'my'}


def load_rows(domain):
    path = os.path.join(DATA, DOMAINS[domain])
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def tokenize(query):
    words = re.split(r'[^a-z0-9%+.\-]+', query.lower())
    return [w for w in words if len(w) > 1 and w not in STOPWORDS]


def score_row(terms, row):
    score = 0
    for key, value in row.items():
        if not value:
            continue
        v = value.lower()
        weight = 3 if key in TITLE_KEYS else 1
        for term in terms:
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


def do_checklist():
    """Print the 40 thumb rules."""
    path = os.path.join(DATA, '..', 'references', 'thumb-rules.md')
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            print(f.read())
    else:
        print('thumb-rules.md not found')


def do_stats():
    total = 0
    print(f"{'domain':<18} {'rows':>5}")
    for d in DOMAINS:
        n = len(load_rows(d))
        total += n
        print(f"{d:<18} {n:>5}")
    print('-' * 24)
    print(f"{'TOTAL':<18} {total:>5}")


def main():
    parser = argparse.ArgumentParser(
        description='nativetap — mobile design intelligence search')
    parser.add_argument('query', nargs='?', default=None)
    parser.add_argument('--domain', default=None,
                        help='restrict search to one domain')
    parser.add_argument('--stack', choices=sorted(STACK_DOMAINS),
                        default=None,
                        help='route to the domains relevant for this stack')
    parser.add_argument('--max-results', type=int, default=3)
    parser.add_argument('--json', action='store_true',
                        help='machine-readable output')
    parser.add_argument('--list-domains', action='store_true')
    parser.add_argument('--checklist', action='store_true',
                        help='print the 40 thumb rules')
    parser.add_argument('--stats', action='store_true',
                        help='rows per domain')
    args = parser.parse_args()

    if args.list_domains:
        if args.json:
            print(json.dumps(sorted(DOMAINS)))
        else:
            print('Available domains:')
            for d in sorted(DOMAINS):
                print(' ', d)
        return
    if args.checklist:
        do_checklist()
        return
    if args.stats:
        do_stats()
        return

    if not args.query:
        parser.print_usage()
        return

    all_domains = sorted(DOMAINS)
    if args.domain:
        if args.domain not in DOMAINS:
            print(f"Unknown domain '{args.domain}'. "
                  f"Available: {', '.join(all_domains)}")
            sys.exit(1)
        domains = [args.domain]
    elif args.stack:
        domains = STACK_DOMAINS[args.stack]
    else:
        domains = all_domains

    terms = tokenize(args.query)
    results = []
    for domain in domains:
        try:
            rows = load_rows(domain)
        except FileNotFoundError:
            continue
        for row in rows:
            s = score_row(terms, row)
            if s > 0:
                results.append((s, domain, row))

    results.sort(key=lambda x: -x[0])
    if not results:
        print(f"No matches for '{args.query}'. Try --list-domains.")
        if not args.json:
            sys.exit(2)
        print(json.dumps([]))
        return

    out = [{'domain': d, 'title': title_of(r), 'row': r, 'score': s}
           for s, d, r in results[:args.max_results]]
    if args.json:
        print(json.dumps(out, indent=2))
        return
    for item in out:
        print(format_row(item['domain'], item['row']))
        print()


if __name__ == '__main__':
    main()
