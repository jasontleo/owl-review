"""Builds the owl review stepper SVGs: one file per state, outlined chips, state-colored borders."""
import pathlib, sys
OUT = pathlib.Path(sys.argv[1])
C = {"done": "#2ea043", "active": "#388bfd", "pending": "#8c959f", "warn": "#db6d28", "skip": "#8957e5"}
NARROW = set("iljtf.,:;'|!·() ")
def tw(s, size=12):
    w = 0
    for ch in s:
        if ch in NARROW: w += 0.30
        elif ch.isupper() or ch in "mwMW": w += 0.68
        elif ch.isdigit(): w += 0.56
        else: w += 0.54
    return w * size
H, PADX, GAP, ARW, OWL = 24, 10, 6, 14, 19
def chip(x, label, color, dashed=False):
    w = tw(label) + 2 * PADX
    dash = ' stroke-dasharray="3 2"' if dashed else ""
    return (f'<rect x="{x+0.75:.2f}" y="2.75" width="{w-1.5:.2f}" height="{H-5.5:.2f}" rx="9.25" fill="none" stroke="{color}" stroke-width="1.5"{dash}/>'
            f'<text x="{x+w/2:.2f}" y="{H/2+4.2:.2f}" text-anchor="middle" class="t">{label}</text>'), w
def arrow(x):
    y = H / 2
    return f'<path d="M{x+2} {y}h{ARW-6}m-3.5 -3.5l3.5 3.5l-3.5 3.5" fill="none" stroke="#8c959f" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>', ARW
def build(name, steps):
    parts, x = [], 0
    parts.append(f'<text x="0" y="{H/2+6.5:.2f}" font-size="{OWL}">🦉</text>'); x = OWL + 6
    for i, (label, kind) in enumerate(steps):
        if i: s, w = arrow(x); parts.append(s); x += w + 2
        s, w = chip(x, label, C["pending" if kind == "dashed" else kind], kind == "dashed"); parts.append(s); x += w + 2
    W = int(x + 1)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{" → ".join(l for l, _ in steps)}">'
           '<style>.t{font:500 12px -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif;fill:#1f2328}'
           '@media (prefers-color-scheme:dark){.t{fill:#e6edf3}}</style>' + "".join(parts) + '</svg>')
    (OUT / f"{name}.svg").write_text(svg)
S = ("Start", "done")
build("reviewing", [S, ("Reviewing", "active"), ("Verdict", "dashed")])
build("approved", [S, ("Reviewed", "done"), ("Approved", "done")])
for n in range(1, 10):
    build(f"address-{n}", [S, ("Reviewed", "done"), (f"{n} to address", "warn")])
build("address-9plus", [S, ("Reviewed", "done"), ("9+ to address", "warn")])
build("head-moved", [S, ("Head moved", "skip"), ("Next pass", "dashed")])
build("merged-first", [S, ("Merged first", "skip")])
build("closed-first", [S, ("Closed first", "skip")])
build("skipped", [S, ("Skipped", "skip")])
(OUT / "owl.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 28 28" role="img" aria-label="owl"><text x="14" y="22" font-size="23" text-anchor="middle">🦉</text></svg>\n')
print(sorted(p.name for p in OUT.iterdir()))
