#!/usr/bin/env python3
"""nativetap audit — scan source files for mobile rule violations.

Usage:
  python audit.py path/to/screen.dart           # one file
  python audit.py lib/                          # directory (recursive)
  python audit.py screen.dart --json

Checks are regex heuristics derived from the data rows + thumb rules:
P0 violations exit 1 so you can use it as a pre-commit / CI gate.
"""
import argparse
import json
import os
import re
import sys

CHECKS = [
    # (id, severity P0-P5, regex, message, fix_domain)
    ("target-small", "P0",
     r"IconButt(?:on|)\b[^;]{0,120}",
     "IconButton found: default 48dp ok, but any SizedBox'd icon button under 44pt fails — check hit area",
     "a11y"),
    ("hardcoded-top-submit", "P1",
     r"mainAxisAlignment:\s*MainAxisAlignment\.end.*?\n.*?(Submit|Pay|Save|Buy|Send)",
     "Primary action placed at the END of a top Row — move to bottom thumb zone",
     "components"),
    ("fixed-height-text", "P0",
     r"height:\s*\d+,(?:(?!height:)[\s\S]){0,300}?(TextField|Text\()",
     "Fixed height around text input/body text: clips at 200% font scale. Flexible heights",
     "a11y"),
    ("keyboard-no-resize", "P0",
     r"resizeToAvoidBottomInset:\s*false",
     "resizeToAvoidBottomInset: false with form fields = keyboard covers the focused field",
     "safe-areas"),
    ("onchanged-validate", "P2",
     r"onChanged.*?(errorText|_error|setError)",
     "Setting errors per keystroke — validate on blur/submit instead",
     "forms"),
    ("web-hex-colors", "P3",
     r"Color\(0xFF[0-9A-Fa-f]{6}\)",
     "Raw hex color: use ColorScheme/semantic tokens, especially for success/warning/error",
     "color"),
    ("no-haptic-success", "P3",
     r"(onSuccess|_success|complete\()",
     "Success state change without HapticFeedback call nearby — haptics mark state changes",
     "gestures"),
    ("listview-children", "P0",
     r"ListView\(\s*children",
     "ListView(children:) for dynamic data — use ListView.builder with itemExtent for long lists",
     "flutter"),
    ("no-semantic-label", "P1",
     r"IconButton\((?![^)]{0,200}semanticLabel)",
     "IconButton without semanticLabel: icon-only buttons need labels",
     "a11y"),
    ("deceptive-toast", "P4",
     r"SnackBar\(.*?(content|Text).*?[Ee]rror",
     "Errors as snackbars: payment/auth errors need dialog/full-screen with retry",
     "errors"),
]

SWIFT_CHECKS = [
    ("fixed-frame-text", "P0",
     r"\.frame\(height:\s*\d+\)\s*\n?\s*(?:.*Text|TextField)",
     "Fixed frame around text: clips at Dynamic Type XXL. Use @ScaledMetric/flexible heights",
     "a11y"),
    ("fullscreencover-overuse", "P2",
     r"fullScreenCover",
     "fullScreenCover for everything: prefer sheet + presentationDetents to preserve context",
     "swiftui"),
    ("ignores-safe-area", "P2",
     r"ignoresSafeArea\(\.all\)",
     "ignoresSafeArea(.all): usually you want .container/.keyboard scoped instead",
     "safe-areas"),
]

def scan(path, text, checks, findings):
    lines = text.splitlines()
    for cid, sev, pattern, msg, dom in checks:
        for m in re.finditer(pattern, text, re.MULTILINE | re.DOTALL):
            line = text[:m.start()].count('\n') + 1
            if cid == "fixed-height-text" and "Button" in text[m.start():m.end()+120]:
                continue
            findings.append({"id": cid, "severity": sev, "file": path,
                             "line": line, "message": msg, "domain": dom,
                             "snippet": text[m.start():m.end()][:120].replace(chr(10), " | ")})

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('path')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()

    targets = []
    if os.path.isdir(args.path):
        for root, _, files in os.walk(args.path):
            targets += [os.path.join(root, f) for f in files
                        if f.endswith(('.dart', '.swift', '.kt'))]
    else:
        targets = [args.path]

    findings = []
    for path in targets:
        try:
            text = open(path, encoding='utf-8', errors='ignore').read()
        except OSError:
            continue
        if path.endswith('.swift'):
            scan(path, text, SWIFT_CHECKS, findings)
        scan(path, text, CHECKS, findings)  # dart/kotlin use the generic set

    sev_order = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3, 'P4': 4, 'P5': 5}
    findings.sort(key=lambda f: (sev_order[f['severity']], f['file'], f['line']))

    if args.json:
        print(json.dumps(findings, indent=1))
    else:
        if not findings:
            print('No nativetap rule violations found. (Heuristic — search the data for full rules.)')
            return
        for f in findings:
            print(f"[{f['severity']}] {f['file']}:{f['line']} — {f['message']}")
            print(f"    → {f['snippet'].strip()}")
            print(f"    domain: {f['domain']}  (search: python3 search.py '<topic>' --domain {f['domain']})")
            print()
        p0 = sum(1 for f in findings if f['severity'] == 'P0')
        print(f"{len(findings)} findings ({p0} P0 blocking)")

    sys.exit(1 if any(f['severity'] == 'P0' for f in findings) else 0)

if __name__ == '__main__':
    main()
