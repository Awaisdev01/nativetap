# Store assets checklist

Every asset both stores will ask for, with exact sizes. Generate the
listing copy with `shipcheck listing`.

## App icon

- [ ] 1024×1024 iOS App Store icon (PNG, no alpha, no rounded corners)
- [ ] 180×180 @3x home icon (system applies the squircle mask)
- [ ] Android adaptive icon: 108dp foreground with 66dp safe zone
- [ ] Android legacy 192×192 for old launchers
- [ ] 512×512 Play Store icon
- [ ] Android notification icon: 24dp, white + alpha ONLY (colored = gray blob)
- [ ] iOS 18 tinted + dark variants (optional but expected in 2026)

## Screenshots

- [ ] iPhone 6.9" (1320×2868) — App Store required
- [ ] iPhone 6.5" if supporting older devices
- [ ] iPad 13" if universal
- [ ] Android phone 16:9 or 9:16 (min 320px, max 3840px)
- [ ] Android 7"/10" tablet if targeting tablets
- [ ] First 2 screenshots sell the app — most users never swipe past them
- [ ] Captions on screenshots (55 chars or fewer each)

## Listing copy (generate with shipcheck)

- [ ] App name ≤ 30 chars (both stores)
- [ ] iOS subtitle ≤ 30 chars
- [ ] Play short description ≤ 80 chars
- [ ] Keywords string ≤ 100 chars (iOS, comma-separated, no spaces)
- [ ] Privacy policy URL — live and reachable
- [ ] Support URL working

## Data safety

- [ ] App Privacy form (App Store) answers match actual SDK behavior
- [ ] Data Safety form (Play) same
- [ ] Account deletion path exists if the app has accounts (both stores require)
