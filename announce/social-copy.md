# X/Twitter thread

1/ AI agents can build an app in a day. They still ship web patterns to
phone screens. So I built nativetap — mobile-only design intelligence for
coding agents. 🧵

2/ What's inside: 461 rules across 42 domains — 40 Thumb Rules with exact
numbers (44pt targets, contrast in both modes, Dynamic Type at 200%), HIG +
Material 3 specs, gestures with haptics pairing, safe-areas in
Flutter/SwiftUI/Compose, motion durations.

3/ Zero dependencies: CSVs + a dependency-free Python search. Works
offline. SKILL.md format — Claude Code, Cursor, Codex, Windsurf,
Antigravity, Copilot.

4/ The fresh part: CI fingerprints live HIG/M3 pages monthly and opens a
review issue when Apple or Google change something. Curated data with
receipts, plus a CI data-integrity check on every PR.

5/ A worked example ships in the repo: the same Flutter checkout screen
with and without nativetap — every fix cited to the exact row.

6/ It's stage 1 of a pipeline: nativetap (design) → promptguard (test the
AI features) → shipcheck (launch audit + store kit). All MIT, all free.

7/ Repo: https://github.com/awaisdev5765/nativetap — PRs adding verified
rows to the CSVs are the highest-value contributions.
