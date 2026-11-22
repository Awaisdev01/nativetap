<div align="center">

<img src="assets/hero.png" alt="nativetap — the mobile design rulebook for AI coding agents" width="100%">

**The mobile design rulebook for AI coding agents.**

464 curated rules · 42 domains · 40 thumb rules · 0 dependencies

[![Claude Code](https://img.shields.io/badge/Claude_Code-skill-8b5cf6)](https://claude.com/claude-code)
[![MCP](https://img.shields.io/badge/MCP-server-3b82f6)](mcp/README.md)
[![CI](https://github.com/awaisdev5765/nativetap/actions/workflows/ci.yml/badge.svg)](https://github.com/awaisdev5765/nativetap/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![v1.1.0](https://img.shields.io/badge/version-1.1.0-blue)](https://github.com/awaisdev5765/nativetap/releases)

*Claude Code · Cursor · Codex · Windsurf · Antigravity · Kiro · Copilot · any MCP client*

[Install](#install) · [Audit your code](#audit-your-own-code) · [What's inside](#whats-inside) · [FAQ](#faq)

</div>

---

Your AI writes great web UI. On phone screens it **guesses** — buttons in
thumb-unreachable corners, lists that jank, back gestures that break, dark
mode that fails contrast, keyboards that cover the field being typed into.

nativetap is the fix. It's a skill (SKILL.md + searchable CSVs) your agent
reads **before writing any mobile UI** — and it doesn't just describe the
rules, it **enforces them with a linter**:

```
search the rules → design the screen → audit the code → CI gate
```

No other mobile design skill closes that loop.

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
**nativetap** (design) → **prism_doctor** (code audit) → **shipcheck** (launch audit)

## Install

<details open>
<summary><b>Claude Code / Antigravity / Kiro</b> (plugin manifest included)</summary>

```bash
git clone https://github.com/awaisdev5765/nativetap.git ~/.claude/skills/nativetap
```

Or into a single project:

```bash
git clone https://github.com/awaisdev5765/nativetap.git .claude/skills/nativetap
```
</details>

<details>
<summary><b>Cursor / Codex / Windsurf</b></summary>

Copy `SKILL.md` + `data/` + `scripts/` + `references/` into your agent's
rules directory — the format is the cross-agent SKILL.md standard.

Cursor users: the repo ships a [`.cursorrules`](.cursorrules) too —
just clone and open the folder.
</details>

<details>
<summary><b>Any MCP client</b> (Claude Desktop, Claude Code, Cursor, Codex, …)</summary>

```json
{
  "mcpServers": {
    "nativetap": {
      "command": "python3",
      "args": ["/absolute/path/to/nativetap/mcp/server.py"]
    }
  }
}
```

Exposes `search_mobile_rules`, `list_domains`, and `thumb_rules` tools —
see [`mcp/README.md`](mcp/README.md). Zero dependencies.
</details>

**Verify it works:**

```bash
python3 .claude/skills/nativetap/scripts/search.py "touch target" --max-results 1
```

## Audit your own code

The skill ships a static analyzer that flags web-instinct violations in
**Dart, Swift, and Kotlin**:

```bash
# Scan a project:
python3 .claude/skills/nativetap/scripts/audit.py lib/

# P0 violations exit 1 — drop it in CI as a ship gate:
python3 .claude/skills/nativetap/scripts/audit.py lib/ || echo "fix P0s before shipping"
```

| Catches | Why it matters |
|---|---|
| Fixed heights around text | Clips at 200% font scale (P0) |
| Primary action in a top Row | Thumb-unreachable one-handed |
| `resizeToAvoidBottomInset: false` | Keyboard covers the focused field |
| Per-keystroke validation errors | Users get red X's while typing |
| `ListView(children:)` on dynamic data | Jank on long lists |
| Raw hex colors | Breaks dark mode + semantic color |
| Unlabeled `IconButton`s | Screen-reader users hit ghosts |
| `ignoresSafeArea(.all)` | Content under the notch/Island |

CI verifies the auditor itself on every push: the bad example **must fail**,
the good one **must pass**.

**New: quiz mode.** An agent can *prove* its mobile literacy — the quiz is
generated from the data rows themselves, and wrong answers name the exact
domain to study:

```bash
python3 .claude/skills/nativetap/scripts/quiz.py --n 10 --stack flutter
# "Your agent is guessing on mobile. Install nativetap and retry." — or:
# "Agent certified: nativetap-literate. Trust it with phone screens."
```

## Usage

Once installed, your agent picks it up automatically when you design or
review mobile UI. You can also drive the search directly:

```bash
python3 search.py "touch target"                 # search everything
python3 search.py "dark mode" --domain color     # one domain
python3 search.py "swipe" --stack flutter        # your stack's ~26 domains
python3 search.py --stats                        # 464 rows across 42 domains
python3 search.py --json "paywall"               # machine-readable
```

In conversation, just ask your agent:

> "Is this list implementation going to jank?" → searches `flutter`
> "What's the iOS convention for destructive swipe actions?" → searches `hig-ios`
> "Make my dark mode correct" → searches `color`, checks the P0 rules

## What's inside

**464 rows across 42 domains**, each with per-platform columns where
platforms differ:

| | | |
|---|---|---|
| **The 40 Thumb Rules** P0–P5 | `flutter` 16 wrong→right patterns | `swiftui` 10 patterns |
| `kotlin` Compose perf + predictive back | `hig-ios` component specs | `material3` M3 specs |
| `gestures` + haptics pairing | `safe-areas` notch/Island/keyboard | `typography` pt/sp scale |
| `color` dark mode + contrast | `motion` durations per platform | `icons` every store size |
| `styles` 49 visual styles | `a11y` screen reader + 200% type | `performance` cold start/jank |
| `forms` keyboard/OTP/autofill | `components` measurable specs | `notifications` timing/channels |
| `tablet-foldable` 600dp+/hinge | `store` screenshots/keywords/A-B | `navigation` 10 IA patterns |
| `offline` cache-first UI | `onboarding` time-to-value | `monetization` paywall timing |
| `widgets-watch` WidgetKit budgets | `animations` springs/easing | `images` blurhash/camera |
| `security` keychain/FLAG_SECURE | `deep-links` Universal/App Links | `push` lifecycle |
| `i18n` RTL/plurals/expansion | `testing` golden/a11y audits | `release` staged rollout |
| `camera` / `maps` / `audio-haptics` | `compose3` typed nav/previews | `visionos` spatial UI |
| `iap` StoreKit 2/refunds | `errors` human error copy | `app-clips` / `voiceover` / `charts` |

Zero dependencies. Pure CSV + a dependency-free search script. Works offline.

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

## A worked example

[`example/checkout_screen/`](example/checkout_screen/) shows a Flutter
checkout screen written **without** nativetap (web instincts: top-right
submit, fixed heights, no haptics) and the **same screen with it** — every
fix cited to the exact row that drove it. Then the auditor confirms:

```bash
$ python3 scripts/audit.py example/checkout_screen/without_nativetap.dart
[P0] Fixed height around text: clips at 200% font scale
[P1] Primary action placed at the END of a top Row — move to bottom thumb zone
2 findings (1 P0 blocking)        # exit 1

$ python3 scripts/audit.py example/checkout_screen/with_nativetap.dart
No nativetap rule violations found.  # exit 0
```

## Data freshness

Fair question: *do the CSVs go stale when HIG or Material 3 update?*

Every source is fingerprinted and version-stamped:

- [`data/VERSION.json`](.claude/skills/nativetap/data/VERSION.json) — last
  reviewed date + which upstream docs each domain was verified against
  (currently: iOS 18/iPadOS 18 HIG + iOS 26 Liquid Glass, M3 + Expressive shapes)
- A monthly CI workflow re-hashes the Apple HIG and Material 3 pages; when
  they change, a review issue opens automatically
- Updates land as auditable diffs — every rule stays traceable to its source
- CI also re-verifies data integrity (parse + column consistency) on every PR

## FAQ

**Are iOS and Android conventions kept apart, or averaged?**
Kept apart. Every cross-platform domain has per-platform columns (iOS /
Android / Flutter / SwiftUI / Compose), so the agent gets the exact HIG or
Material spec — not a mushy middle. Where platforms genuinely agree, the row
is shared; where they differ (back gesture, nav patterns), each keeps its
own rule.

**Does this replace a designer?**
No — it stops the AI from breaking the platform's hard rules (thumb reach,
contrast, safe areas, gesture conflicts). The taste is still yours.

**Why CSVs and not a bigger format?**
Plain data + a dependency-free search script = works offline, in any agent,
forever. No SDK, no lock-in, no breakage. And plain data means anyone can
audit a row in 30 seconds.

## The pipeline

nativetap is one third of a full "vibe coder ships a real app" toolkit:

| Stage | Tool | What it checks |
|---|---|---|
| **Design** | **nativetap** (this skill) | HIG/M3 correctness, thumb ergonomics, platform patterns |
| Code | [prism_doctor](https://pub.dev/packages/prism_doctor) | Hardcoded colors, magic numbers, deprecated imports |
| Launch | [shipcheck](https://pub.dev/packages/shipcheck) | Store listings, privacy, screenshots, release notes |

## Contributing

**The data files are the product** — PRs adding rows to the CSVs (with
correct, verified platform data) are the highest-value contribution. Each
row is small and sourced, so a PR per HIG/Material release is cheap and
reviewable. See [`CONTRIBUTING.md`](CONTRIBUTING.md); stale rows can be
reported with the ["Stale or wrong data row"](../../issues/new?template=stale-row.yml)
issue template.

## More from this ecosystem

| | Tool |
|---|---|
| 📡 **New** | [smsaria](https://github.com/awaisdev5765/smsaria) — open-source AI gateway for basic phones (SMS + USSD) |
| Design | [nativetap](https://github.com/awaisdev5765/nativetap) — mobile design intelligence |
| Shell | [bashproof](https://github.com/awaisdev5765/bashproof) — agent-proof quoting |
| Audit | [diffconscience](https://github.com/awaisdev5765/diffconscience) — pre-handoff diff audit |
| Launch | [shipcheck](https://pub.dev/packages/shipcheck) — release-readiness |
| AI features | [promptguard](https://pub.dev/packages/promptguard) — prompt regression tests |

## License

MIT — see [LICENSE](LICENSE).
