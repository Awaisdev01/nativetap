# Show HN draft — nativetap

**Title:** Show HN: Nativetap – mobile UI design intelligence for AI coding agents

**Text post:**

I kept watching AI agents build mobile apps that *look* right but break every
platform convention — Android navigation patterns on iOS, 32px touch targets,
keyboards covering form fields, placeholder text standing in for labels.

The existing design skills are web-first. The biggest one covers 22 stacks and
serves mobile as one row of its data. So I built nativetap: a skill that is
*exclusively* about what users touch with their thumbs.

What's in it:

- The 40 Thumb Rules — prioritized P0 (non-negotiable: ≥44pt targets, contrast
  in both modes, Dynamic Type at 200%) to P5 (ship-blocking), each with exact
  numbers
- 12 searchable data domains: Flutter/SwiftUI/Jetpack Compose patterns
  (wrong→right with why), Apple HIG component specs, Material 3 specs,
  gesture conventions with haptics pairing, safe-area handling in all 3
  frameworks, mobile type scale, dark-mode color rules, motion durations,
  app-icon sizes for every store
- Zero dependencies: CSVs + a ~200-line Python search. Works offline.
- SKILL.md format — works with Claude Code, Cursor, Codex, Windsurf,
  Antigravity

Your agent picks it up automatically when you design or review mobile UI.

```
python3 skills/nativetap/scripts/search.py "touch target" --domain flutter
```

It's also the design stage of a pipeline: nativetap (design) → prism_doctor
(code audit) → shipcheck (launch audit).

Data freshness: every file is version-stamped, and CI fingerprints the live
HIG/Material pages monthly, opening a review issue when upstream changes —
so the answer to "do you refresh when Apple updates the HIG?" is yes, with
receipts.

Repo: https://github.com/awaisdev5765/nativetap

Happy to answer questions — especially from anyone who's shipped an app
their agent designed.
