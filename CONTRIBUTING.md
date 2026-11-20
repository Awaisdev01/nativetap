# Contributing to nativetap

The **data files are the product**. The highest-value contribution is a
verified row added to the right CSV.

## Adding data rows (the main way to help)

1. Pick the domain that fits (see the table in the README, or run
   `python3 scripts/search.py --list-domains`).
2. Add **one row** to the domain's CSV in
   `.claude/skills/nativetap/data/` — keep the existing column order.
3. The row must be **verifiable**: cite the Apple HIG page, Material 3
   spec, or official framework doc it comes from in your PR description.
   A number without a source gets asked about, and we'd rather ask up front.
4. One row per PR is fine; small PRs review fast.

## Rules for rows

- **Per-platform, not averaged.** If iOS and Android differ, both get their
  own value/column. Never write a "middle" convention.
- **Exact numbers over adjectives.** `250ms` beats "fast". `44pt` beats "big enough".
- **Wrong → right beats abstract.** If your row describes a mistake, say the
  correct pattern in the same row.
- **Mobile only.** Web-only patterns (Tailwind, responsive breakpoints,
  browser APIs) don't belong here.

## Search script changes

`scripts/search.py` is dependency-free Python 3 and must stay that way.
New flags welcome; new dependencies are not.

## Upstream freshness

If Apple HIG or Material 3 shipped a change that makes a row stale, open an
issue referencing the domain and row — the monthly freshness CI will have
flagged upstream changes too, but human eyes catch what hashing can't.

## License

By contributing you agree your contributions are licensed under MIT.
