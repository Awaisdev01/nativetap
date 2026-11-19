---
name: nativetap
description: "Mobile UI/UX design intelligence for iOS, Android, Flutter, SwiftUI, and Kotlin. This skill should be used when designing, building, reviewing, or fixing MOBILE interfaces: screens, components, platform conventions (Apple HIG / Material 3), gestures, safe areas, typography scales, dark mode, motion, app icons, and stack-specific implementation patterns (Flutter, SwiftUI, Jetpack Compose). Searchable local data: 40 thumb rules, 10 mobile styles, gesture conventions with haptics pairing, safe-area handling per platform, 16 Flutter patterns, SwiftUI and Kotlin patterns, HIG and Material 3 component specs, mobile typography scales, dark-mode color rules, motion specs with durations, and app icon sizes for every platform and store. Skip it for web-only work (Tailwind, responsive breakpoints, browser APIs) — this skill is exclusively about what users touch with their thumbs."
---

# nativetap — Mobile Design Intelligence

The mobile-only counterpart to web-first design skills. Every data file,
every rule, every pattern is about **what users touch with their thumbs**.

## When to Apply

- Designing or reviewing mobile screens (any framework)
- Choosing between iOS HIG vs Material 3 conventions
- Implementing Flutter/SwiftUI/Jetpack Compose screens correctly
- Fixing "this feels off" mobile UX (gestures, keyboard, safe areas, haptics)
- Preparing store assets (icons, screenshots)
- Auditing an app before release (pairs with the shipcheck audit)

Skip for: web-only UI, backend logic, desktop-only apps.

## The 40 Thumb Rules

Read `references/thumb-rules.md` — priority P0 (non-negotiable) to P5
(ship-blocking). Always check a design against P0+P1 before delivering.

Top rules (full list in the reference):

| Priority | Rule | Numbers |
|---|---|---|
| P0 | Touch targets | ≥ 44×44pt iOS / 48×48dp Android |
| P0 | Contrast | ≥ 4.5:1 body, 3:1 large — check BOTH modes |
| P0 | Dynamic Type | Layout survives 200% text scale |
| P1 | Feedback latency | ≤ 100ms visible response to every tap |
| P1 | Keyboard | Pushes content, never covers the focused field |
| P2 | Navigation matches platform | iOS tabs+back-swipe / Android top bar+system back |
| P2 | Haptics | State changes only (success/error/selection) |
| P3 | Labels above fields | Placeholder-as-label is a bug |
| P5 | Cold start | ≤ 2s to first meaningful paint |

## Searching the Data

```bash
# All 23 domains:
python3 scripts/search.py "touch target size"

# One domain:
python3 scripts/search.py "dark mode elevation" --domain color
python3 scripts/search.py "list performance" --domain flutter

# Route to the domains that matter for a stack:
python3 scripts/search.py "offline" --stack flutter
python3 scripts/search.py "hinge" --stack swiftui

# Machine-readable / diagnostics:
python3 scripts/search.py "paywall" --json
python3 scripts/search.py --stats        # rows per domain
python3 scripts/search.py --checklist    # the 40 thumb rules
python3 scripts/search.py --list-domains
```

## Data Domains

| Domain | File | Contents |
|---|---|---|
| `flutter` | flutter-patterns.csv | 16 wrong→right patterns: lists, images, forms, state, navigation |
| `swiftui` | swiftui-patterns.csv | 10 patterns: NavigationStack, ownership, insets |
| `kotlin` | kotlin-patterns.csv | 10 patterns: Compose perf, ViewModel, predictive back |
| `hig-ios` | hig-ios.csv | Apple HIG component specs (nav bars, sheets, alerts, swipe actions) |
| `material3` | material3.csv | M3 component specs (FABs, nav bar, chips, tonal elevation) |
| `gestures` | gestures.csv | Convention per gesture + haptics pairing + common mistakes |
| `safe-areas` | safe-areas.csv | Notch/Island/home-indicator/keyboard handling in all 3 frameworks |
| `typography` | typography-mobile.csv | Type scale with pt/sp + Flutter tokens |
| `color` | color-mobile.csv | Dark mode, dynamic color, contrast, semantic tokens |
| `motion` | motion.csv | Transition specs with durations per platform |
| `icons` | app-icons.csv | Every icon size for iOS/Android/watch/store |
| `styles` | styles.csv | 49 mobile visual styles with when-to-use/avoid |
| `a11y` | a11y.csv | Screen reader, focus order, live regions, 200% type, color-blind |
| `performance` | performance.csv | Cold start <2s, jank, image decode, memory, battery targets |
| `forms` | forms.csv | Keyboard types, autofill, OTP, validation timing, submit state |
| `components` | components-specs.csv | Measurable spec: bar heights, row heights, FAB, sheet, radius |
| `notifications` | notifications.csv | Permission timing, channels, deep links, badges, actions |
| `tablet-foldable` | tablet-foldable.csv | Two-pane 600dp+, hinge, window resize, stylus, shortcuts |
| `store` | assets-store.csv | Screenshot strategy, keywords, feature graphic, A/B tests |
| `navigation` | navigation-ia.csv | 10 IA patterns: tabs, drawer, hub-spoke, deep-link-first |
| `offline` | networking-offline.csv | Cache-first UI, retry backoff, optimistic updates, sync |
| `onboarding` | onboarding-retention.csv | Time-to-value, progressive disclosure, D1/D7 hooks |
| `monetization` | monetization.csv | Paywall timing, trials, restore, store-compliant CTAs |


## Workflow

1. **Design**: search `styles` for the visual direction; check `thumb-rules` P0.
2. **Build**: search the framework domain for the pattern you're about to write
   (e.g. `--domain flutter "list"` before writing any list code).
3. **Platform-check**: consult `hig-ios` / `material3` when implementing
   navigation, sheets, or system components.
4. **Polish**: `motion` for transition durations, `gestures` for haptics pairing,
   `color` for dark mode verification.
5. **Ship**: `icons` for asset sizes; run the store-asset checklist in
   `references/store-checklist.md`.

## The audit pipeline

nativetap is the design stage of a full shipping pipeline:

- **nativetap** (this skill) — design & build it right
- **prism_doctor** — audit the code against design-system rules
- **shipcheck** — audit launch-readiness & generate store assets
