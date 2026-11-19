# 📱 nativetap

**Mobile UI/UX design intelligence for AI coding agents.**

The mobile-only design skill: Apple HIG, Material 3, Flutter/SwiftUI/Kotlin
patterns, gestures, safe areas, dark mode, motion specs, and store assets —
as searchable local data your agent can query instantly.

Works with **Claude Code, Cursor, Codex, Windsurf, Antigravity, Kiro, Copilot**
— any agent that reads SKILL.md files.

![nativetap search in the terminal](assets/search.png)

## Why nativetap

Existing design skills are web-first. The biggest one (150k+ ⭐) covers 22
stacks — but mobile is one row in its data, and its flagship content is
Tailwind, React, and landing pages. Meanwhile:

- **2M+ Flutter developers** get shallow coverage
- iOS HIG and Material 3 are *platform contracts*, not style suggestions
- Mobile has hard constraints web doesn't: 44pt touch targets, thumb zones,
  safe areas, gesture conflicts, haptics semantics
- Store rejection is a real tax (icon sizes, data-safety forms)

nativetap is **exclusively about what users touch with their thumbs** — and
it's the design stage of a complete shipping pipeline:

```
nativetap (design) → prism_doctor (code audit) → shipcheck (launch audit)
```

## What's inside

| Data domain | Contents |
|---|---|
| **The 40 Thumb Rules** | Priority P0–P5, each with the exact numbers |
| `flutter` | 16 wrong→right patterns: lists, images, forms, state, navigation |
| `swiftui` | 10 patterns: NavigationStack, ownership, insets, accessibility |
| `kotlin` | 10 patterns: Compose perf, ViewModel, predictive back |
| `hig-ios` | Apple component specs: nav bars, sheets, alerts, swipe actions |
| `material3` | M3 specs: FABs, nav bar, chips, tonal elevation |
| `gestures` | Convention per gesture + haptics pairing + common mistakes |
| `safe-areas` | Notch/Island/home-indicator/keyboard in all 3 frameworks |
| `typography` | Mobile type scale with pt/sp + Flutter tokens |
| `color` | Dark mode rules, dynamic color, contrast, semantic tokens |
| `motion` | Transition specs with exact durations per platform |
| `icons` | Every icon size: iOS/Android/watch/store |
| `styles` | 10 mobile visual styles with when-to-use/avoid |

Zero dependencies. Pure CSV + a search script. Works offline.

## Install

### Claude Code / Antigravity / Kiro (plugin manifest included)

```bash
git clone https://github.com/awaisdev5765/nativetap.git ~/.claude/skills/nativetap
```

Or add to your project:

```bash
git clone https://github.com/awaisdev5765/nativetap.git .claude/skills/nativetap
```

### Cursor / Codex / Windsurf

Copy `SKILL.md` + `data/` + `scripts/` + `references/` into your agent's
rules directory — the format is the cross-agent SKILL.md standard.

## Usage

Once installed, your agent picks it up automatically when you design or
review mobile UI. You can also drive the search directly:

```bash
# Search everything:
python3 .claude/skills/nativetap/scripts/search.py "touch target"

# Search one domain:
python3 .claude/skills/nativetap/scripts/search.py "list performance" --domain flutter
python3 .claude/skills/nativetap/scripts/search.py "dark mode" --domain color
python3 .claude/skills/nativetap/scripts/search.py "swipe" --domain gestures

# What data exists:
python3 .claude/skills/nativetap/scripts/search.py --list-domains
```

In conversation, just ask your agent:

> "Is this list implementation going to jank?" → searches `flutter` domain
> "What's the iOS convention for destructive swipe actions?" → searches `hig-ios`
> "Make my dark mode correct" → searches `color`, checks the 40 rules P0

## The 40 Thumb Rules (sneak peek)

| Priority | Rule | Numbers |
|---|---|---|
| **P0** | Touch targets | ≥ 44×44pt iOS / 48×48dp Android |
| **P0** | Contrast | ≥ 4.5:1 body — check BOTH light and dark mode |
| **P0** | Dynamic Type | Layout must survive 200% text scale |
| **P1** | Tap feedback | Visible response ≤ 100ms |
| **P1** | Keyboard | Pushes content, never covers the focused field |
| **P1** | Long-press | Reveals, never deletes |
| **P2** | Navigation matches platform | iOS tabs+back-swipe / Android top bar+system back |
| **P2** | Haptics | Mark state changes, never decorate |
| **P3** | Form labels | Above fields, always visible |
| **P5** | Cold start | ≤ 2s to first meaningful paint |

All 40 with rationale in
[`references/thumb-rules.md`](.claude/skills/nativetap/references/thumb-rules.md).

## The pipeline

nativetap is one third of a full "vibe coder ships a real app" toolkit:

| Stage | Tool | What it checks |
|---|---|---|
| **Design** | **nativetap** (this skill) | HIG/M3 correctness, thumb ergonomics, platform patterns |
| Code | [prism_doctor](https://pub.dev/packages/prism_doctor) | Hardcoded colors, magic numbers, deprecated imports |
| Launch | [shipcheck](https://pub.dev/packages/shipcheck) | Store listings, privacy, screenshots, release notes |

## Contributing

The data files are the product — PRs adding rows to the CSVs (with correct,
verified platform data) are very welcome. Search script is dependency-free
Python 3.

## License

MIT — see [LICENSE](LICENSE).
