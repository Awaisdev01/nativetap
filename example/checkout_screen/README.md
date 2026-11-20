# Example: checkout screen, built with nativetap

A minimal Flutter checkout screen demonstrating rows the agent would pull
from the skill — vs the same screen written without it.

| Without nativetap (web instinct) | With nativetap (row applied) |
|---|---|
| Submit button top-right | Primary action bottom, in the thumb zone (`components`, thumb rule #2) |
| 32pt tap targets | 48dp minimum + 8px spacing (`a11y`, thumb rule #1/#3) |
| Fixed-height text | Flexible heights, survives 200% font scale (`a11y`, thumb rule #6) |
| Red X while typing | Validation on blur/submit (`forms`) |
| No haptic on success | Success = check bounce + light impact (`gestures`, `motion`) |
| Keyboard covers focused field | MediaQuery.viewInsets + resizeToAvoidBottomInset (`safe-areas`, thumb rule #14) |

See `without_nativetap.dart` and `with_nativetap.dart` side by side.
