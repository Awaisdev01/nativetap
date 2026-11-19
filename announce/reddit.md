# Reddit drafts

## r/FlutterDev

**Title:** nativetap — a mobile-only UI/UX skill so your AI agent stops shipping web patterns to phone screens

I build Flutter apps with AI agents and kept getting the same mistakes:
`ListView(children: [...])` for 500 items, Material nav on iOS-shaped apps,
hardcoded 44.0 padding for notches, keyboard covering the focused field.

nativetap is a skill (SKILL.md + searchable CSVs, zero dependencies) your
agent reads when designing or reviewing mobile UI. 16 Flutter wrong→right
patterns, plus HIG/Material 3 specs, gestures with haptics pairing,
safe-areas in Flutter/SwiftUI/Compose, dark-mode rules, motion durations.

Free, MIT: https://github.com/awaisdev5765/nativetap

Install: drop it in `.claude/skills/nativetap` and ask your agent to review
your screens against it.

## r/dartlang

**Title:** I shipped 9 pub.dev packages and a 3-tool kit for AI-assisted devs: nativetap (design) → promptguard (test AI features) → shipcheck (launch audit)

Short story: agents are great at building and terrible at the last mile.

- nativetap — mobile design intelligence skill (HIG, M3, Flutter patterns)
- promptguard — regression tests for your app's AI features, CI-native,
  runs against OpenAI/Anthropic/Gemini/Groq/OpenRouter or self-hosted
- shipcheck — audits launch-readiness (scored A–F) and generates store
  listings, privacy policy worksheet, release notes, landing page

All free + MIT. Links in comments.
