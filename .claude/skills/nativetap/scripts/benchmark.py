#!/usr/bin/env python3
"""nativetap benchmark — grade AI models on mobile-design literacy.

Runs the SAME seeded quiz against multiple models via an OpenAI-compatible
chat API, grades with fuzzy matching, and prints a leaderboard.

Usage:
  export NATIVETAP_API_BASE=https://api.openai.com/v1   # or any OpenAI-compatible endpoint
  export NATIVETAP_API_KEY=sk-...
  python benchmark.py --models gpt-4o,claude-sonnet-4-5 --n 15

  # grade an agent that already answered (offline):
  python benchmark.py --grade-run run.json
"""
import argparse
import json
import os
import sys
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
from quiz import build_bank, make_quiz  # noqa: E402

GRADING_INSTRUCTIONS = (
    "You are being quizzed on mobile UI/UX design conventions (Apple HIG, "
    "Material 3, Flutter, SwiftUI, Jetpack Compose). For each question pick "
    "the correct option. Reply with ONLY a JSON array of integers — the "
    "option number (1 or 2) for each question, in order."
)


def ask_model(base, key, model, questions):
    """Send the quiz in one shot; returns list of ints (1/2 per question)."""
    lines = []
    for i, q in enumerate(questions, 1):
        lines.append(f"Q{i}. {q['question']}\n1) {q['answer']}\n2) {q['distractor']}")
    prompt = GRADING_INSTRUCTIONS + "\n\n" + "\n\n".join(lines)

    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
    }).encode()
    req = urllib.request.Request(
        base.rstrip('/') + '/chat/completions',
        data=body,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        resp = json.load(r)
    text = resp['choices'][0]['message']['content']
    # extract the array — tolerate code fences and prose
    start, end = text.find('['), text.rfind(']')
    picks = json.loads(text[start:end + 1])
    return [int(p) for p in picks]


def score(questions, picks):
    results = []
    for q, p in zip(questions, picks):
        # position of the correct answer depends on the ask order: option 1 = answer
        results.append(p == 1)
    return results


def run():
    ap = argparse.ArgumentParser()
    ap.add_argument('--models', help='comma-separated model names')
    ap.add_argument('--n', type=int, default=15)
    ap.add_argument('--stack', default='design')
    ap.add_argument('--seed', type=int, default=1337)
    ap.add_argument('--api-base', default=os.environ.get('NATIVETAP_API_BASE', ''))
    ap.add_argument('--api-key', default=os.environ.get('NATIVETAP_API_KEY', ''))
    ap.add_argument('--grade-run', help='grade a saved run.json instead of querying')
    ap.add_argument('--out', default='benchmark_results.json')
    args = ap.parse_args()

    bank = build_bank()
    questions = make_quiz(bank, args.n, args.stack, args.seed)
    if not questions:
        print('no questions')
        sys.exit(1)

    if args.grade_run:
        run_data = json.load(open(args.grade_run))
        for entry in run_data:
            picks = entry.get('picks', [])
            results = score(questions, picks)
            entry['score'] = sum(results)
            entry['total'] = len(results)
        run_data.sort(key=lambda e: -e.get('score', 0))
        print(f"{'model':<40} score")
        for e in run_data:
            print(f"{e['model']:<40} {e['score']}/{e['total']}")
        json.dump(run_data, open(args.out, 'w'), indent=1)
        return

    if not (args.models and args.api_base and args.api_key):
        print('Need --models, --api-base (or NATIVETAP_API_BASE), --api-key (or NATIVETAP_API_KEY).')
        print('Any OpenAI-compatible endpoint works (OpenAI, Anthropic via proxy, OpenRouter, local Ollama).')
        sys.exit(1)

    leaderboard = []
    for model in [m.strip() for m in args.models.split(',')]:
        print(f"quizging {model} …", flush=True)
        try:
            picks = ask_model(args.api_base, args.api_key, model, questions)
            results = score(questions, picks)
            leaderboard.append({
                'model': model,
                'picks': picks,
                'score': sum(results),
                'total': len(results),
            })
            print(f"  {model}: {sum(results)}/{len(results)}")
        except Exception as e:
            print(f"  {model}: ERROR {e}")
            leaderboard.append({'model': model, 'error': str(e), 'score': -1,
                                'total': len(questions)})

    leaderboard.sort(key=lambda e: -e['score'])
    print(f"\n{'=' * 46}\nMOBILE DESIGN LITERACY LEADERBOARD (seed {args.seed})")
    for e in leaderboard:
        bar = '█' * max(0, e['score']) + '░' * (len(questions) - max(0, e['score']))
        print(f"  {e['model'][:34]:<34} {bar} {e['score']}/{len(questions)}")
    json.dump({'seed': args.seed, 'n': len(questions),
               'questions': questions, 'results': leaderboard},
              open(args.out, 'w'), indent=1)
    print(f"\nsaved → {args.out}")


if __name__ == '__main__':
    run()
