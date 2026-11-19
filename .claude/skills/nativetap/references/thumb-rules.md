# The 40 Thumb Rules

Mobile-only, priority-ordered. Each rule: what, why, the numbers.

## P0 — Non-negotiable (accessibility & ergonomics)

1. **Touch targets ≥ 44×44pt (iOS) / 48×48dp (Android).** Smaller = mis-taps. Count the *visual* target AND its hit area separately; pad hit areas invisibly.
2. **Primary actions live in the thumb zone.** Bottom ⅓ of the screen = high-reach. Top corners =unreachable anti-pattern for frequent actions (one-handed unreachable).
3. **8px+ spacing between adjacent targets.** Finger error radius is ~5mm; two tappable elements side-by-side under 8px apart cause double-taps.
4. **Contrast ≥ 4.5:1 body text, 3:1 large text & icons.** Check BOTH light and dark mode. Dark mode is not "invert colors" — dim pure whites.
5. **Every icon-only button gets a label.** `semanticLabel` (Flutter), `accessibilityLabel` (SwiftUI), `contentDescription` (Android). No exceptions.
6. **Respect Dynamic Type / font scaling.** Layout must survive 200% text scale: use flexible heights, never fixed-height text containers.
7. **Support reduced motion.** `MediaQuery.disableAnimations` / `UIAccessibility.isReduceMotionEnabled` / `Settings.Global.ANIMATOR_DURATION_SCALE`.
8. **Don't remove focus rings/hit highlights.** They're keyboard & switch-control navigation, not decoration.

## P1 — Interaction correctness

9. **Buttons give feedback within 100ms.** Ripple (Android), highlight (iOS), scale. A tap with zero feedback feels broken even when it works.
10. **Nothing critical on double-tap only.** Double-tap is error-prone; pair with a single-tap alternative.
11. **Swipes don't conflict with scroll.** Horizontal swipe on a vertically-scrolling screen must have >18° angle tolerance or gesture arena wins randomly.
12. **Long-press reveals, never deletes.** Destruction on long-press = accidental data loss (1s accidental hold).
13. **Back always works, everywhere.** Predictive back (Android 14+), swipe-back edge (iOS), hardware back. A screen you can't leave is a bug.
14. **Keyboard pushes, never covers.** `resizeToAvoidBottomInset`, `android:windowSoftInputMode="adjustResize"`, `.keyboard` safe area.
15. **Scroll position survives navigation.** Returning to a list at position 0 loses user context.
16. **Optimistic UI for local actions.** Like/save/favorite = instant visual response, sync in background. 300ms round-trips feel laggy.
17. **Loading ≥ 300ms gets a spinner; ≥ 2s gets progress or skeleton.** Sub-300ms: show nothing (flash otherwise).
18. **Pull-to-refresh is expected on feeds.** Absence = users kill/reopen the app.

## P2 — Platform trust

19. **Navigation matches the platform.** iOS: bottom tabs + back-swipe. Android: Material top app bar + system back. Users punish cross-platform clones with uninstall.
20. **System fonts for body text.** SF Pro / Roboto. Custom fonts = display headings only.
21. **Respect safe areas.** Notches, Dynamic Island, home indicator, gesture bars: `SafeArea`, `.safeAreaInset`, `WindowInsets`.
22. **Haptics mark state changes, not decoration.** Success/error/warning/selection — light impact. Never buzz on scroll.
23. **Native pickers for dates/times.** The platform wheel/sheet is what users know. Custom pickers need a strong reason.
24. **Sheets over full-screen modals.** Bottom sheets (detents) preserve context. Full-screen only for create/edit flows.
25. **Empty states teach.** Empty list = illustration + one sentence + one button. Not a blank screen.

## P3 — Forms & input

26. **Labels above fields, always visible.** Placeholder-as-label disappears on focus — memory tax.
27. **Errors appear inline, next to the field.** Error text + red border + `semanticLabel`. Never a summary dialog.
28. **Correct keyboard per field.** `email`/`number`/`phone`/`url` — a QWERTY for a phone number is a bug.
29. **Auto-advance & auto-format as you type.** Phone numbers, card numbers, OTP codes. Every character the user types twice is churn.
30. **Final field submits the form.** `textInputAction: done → onSubmitted`. Don't make users hunt for the button.

## P4 — Layout & data

31. **One primary action per screen.** Two competing CTAs halve conversion on both.
32. **Lists: fixed-height rows for perf.** `itemExtent` (Flutter), no auto-size rows over 100+ items without caching.
33. **Images: cached, sized, placeholdered.** `cached_network_image` / AsyncImage with placeholder + fade. Raw network images jank scroll.
34. **Numbers align on tabular figures.** `FontFeature.tabularFigures()` — columns of prices must not wobble.
35. **Dark mode is a first-class design, not an afterthought.** Elevation = lighter surfaces, not shadows (shadows vanish on dark).

## P5 — Ship-blocking polish

36. **Launch ≤ 2s cold to first meaningful paint.** Profile before shipping; lazy-load everything non-critical.
37. **All state changes animate ≤ 300ms.** Longer = sluggish. Springs for interactive, ease-out for entrances.
38. **No layout shift after images load.** Reserve aspect ratio (`AspectRatio`, `aspectRatio:`) or watch CLS-style jumps.
39. **Offline-first for reads.** Cache last-good data + banner. Spinners on every open = churn.
40. **Test on the smallest supported device.** iPhone SE / small Android — not just the 15 Pro Max simulator.
