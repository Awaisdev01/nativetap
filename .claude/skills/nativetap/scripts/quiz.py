#!/usr/bin/env python3
"""nativetap quiz — adversarial self-test for AI coding agents.

Generates multiple-choice questions FROM the data rows. An agent (or a
human) takes the quiz; wrong answers reveal exactly which domain to study.
The point: any agent can prove it knows mobile conventions, and team leads
can measure their agent before trusting it with UI work.

Usage:
  python quiz.py                    # 10 questions, interactive
  python quiz.py --n 5 --stack flutter
  python quiz.py --grade answer.json  # grade a non-interactive session
"""
import argparse
import csv
import json
import os
import random
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, '..', 'data')

# question generators per schema shape: (file, question field, answer field, distractor field, fmt)
SOURCES = [
    ('flutter-patterns.csv', 'problem', 'right_pattern', 'wrong_pattern',
     lambda q: f"In Flutter, what is the RIGHT way to handle: {q}?"),
    ('swiftui-patterns.csv', 'problem', 'right_pattern', 'wrong_pattern',
     lambda q: f"In SwiftUI, what is the RIGHT way to handle: {q}?"),
    ('kotlin-patterns.csv', 'problem', 'right_pattern', 'wrong_pattern',
     lambda q: f"In Jetpack Compose, what is the RIGHT way to handle: {q}?"),
    ('gestures.csv', 'gesture', 'convention', 'common_mistakes',
     lambda q: f"What is the platform convention for the '{q}' gesture?"),
    ('color-mobile.csv', 'topic', 'rule', 'details',
     lambda q: f"Mobile dark-mode/contrast rule for '{q}'?"),
    ('performance.csv', 'topic', 'target', 'symptom_if_wrong',
     lambda q: f"What is the target for mobile '{q}'?"),
    ('monetization.csv', 'topic', 'rule', 'mistake',
     lambda q: f"IAP/paywall best practice for '{q}'?"),
    ('onboarding-retention.csv', 'topic', 'rule', 'mistake',
     lambda q: f"Onboarding/retention best practice for '{q}'?"),
    ('errors.csv', 'topic', 'rule', 'bad_example',
     lambda q: f"Error-message design rule for '{q}'?"),
]


def build_bank():
    bank = []
    for fname, qf, af, df, fmt in SOURCES:
        path = os.path.join(DATA, fname)
        if not os.path.exists(path):
            continue
        with open(path, newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                q, a, d = row.get(qf), row.get(af), row.get(df)
                if not (q and a and d) or len(a) < 8:
                    continue
                bank.append({
                    'question': fmt(q),
                    'answer': a,
                    'distractor': d,
                    'domain': fname.replace('.csv', ''),
                    'source_file': fname,
                })
    return bank


def make_quiz(bank, n, stack=None, seed=None):
    if stack:
        keep = {'flutter': ('flutter-patterns', 'gestures', 'color-mobile',
                            'performance', 'errors', 'monetization',
                            'onboarding-retention'),
                'swiftui': ('swiftui-patterns', 'gestures', 'color-mobile',
                            'performance'),
                'kotlin': ('kotlin-patterns', 'gestures', 'performance')} \
            .get(stack)
        if keep:
            bank = [b for b in bank if b['domain'] in keep]
    rng = random.Random(seed or os.urandom(8))
    return rng.sample(bank, min(n, len(bank)))


def ask(q, i, total):
    # 50/50 position so position never leaks the answer
    opts = [q['answer'], q['distractor']]
    rng = random.Random(hash(q['question']) & 0xffff)
    rng.shuffle(opts)
    correct_idx = opts.index(q['answer'])
    print(f"\n[{i + 1}/{total}] ({q['domain']}) {q['question']}")
    for j, o in enumerate(opts, 1):
        print(f"  {j}) {o}")
    try:
        pick = input("  your answer (1/2): ").strip()
    except EOFError:
        pick = '0'
    got = {'1': 0, '2': 1}.get(pick, -1)
    correct = got == correct_idx
    if not correct:
        print(f"  ✗ Wrong. The right pattern: {q['answer']}")
        print(f"    → study: search.py '<topic>' --domain {q['domain']}")
    else:
        print("  ✓ Correct")
    return correct


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=10)
    ap.add_argument('--stack', choices=['flutter', 'swiftui', 'kotlin'])
    ap.add_argument('--grade', help='JSON file of answers to grade')
    ap.add_argument('--seed', help='pin the quiz sample (required with --grade)')
    ap.add_argument('--json-out', help='write questions+answers as JSON (for agent self-test)')
    args = ap.parse_args()

    bank = build_bank()
    seed = int(args.seed) if args.seed else None
    quiz = make_quiz(bank, args.n, args.stack, seed)
    if not quiz:
        print('No questions available.')
        sys.exit(1)

    if args.json_out:
        json.dump([{k: v for k, v in q.items()} for q in quiz],
                  open(args.json_out, 'w'), indent=1)
        print(f'wrote {len(quiz)} questions to {args.json_out}')
        return

    if args.grade:
        answers = json.load(open(args.grade))
        correct = 0
        for q, a in zip(quiz, answers):
            # grade by substring match against the answer text
            correct += int(str(a).strip().lower() in q['answer'].lower())
        print(f"{correct}/{len(quiz)} correct")
        sys.exit(0 if correct == len(quiz) else 1)

    score = sum(ask(q, i, len(quiz)) for i, q in enumerate(quiz))
    pct = 100 * score // len(quiz)
    print(f"\n{'=' * 40}\nScore: {score}/{len(quiz)} ({pct}%)")
    if pct == 100:
        print("Agent certified: nativetap-literate. Trust it with phone screens.")
    elif pct >= 70:
        print("Decent — review the flagged domains above.")
    else:
        print("Your agent is guessing on mobile. Install nativetap and retry.")


if __name__ == '__main__':
    main()
