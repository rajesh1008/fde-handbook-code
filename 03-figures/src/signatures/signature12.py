"""Signature 12: the test pyramid, hand-laid SVG (BOOK-PROMPT rev 003.1, Part C; Part A figure rules 1 and 4).
Five layers stacked from unit (widest, cheapest, every commit) to operational (narrowest, the live stream). Each band
carries its layer, its frequency and its cost per run; the merge gate spans the layers that can block a merge. One
template for every recurrence: identical layout, scale and palette; the layers named in state["changed"] (1 to 5, or
"gate") are drawn in the emphasis stroke (2.5 pt). A chapter adds its state to STATES and calls render(state, stem,
source).

State: dict(version=str, rows=[(name, frequency, cost) x 5, bottom layer first], foot=str, changed=tuple).
"""
import sys, pathlib, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "05-build/design"))
import fde_style as S, fde_svg

W = 396; PAD = 12; F_SANS = "Source Sans Pro"
ROLES = ("system", "model", "data", "evidence", "approval")
STATES = {}


def _t(x, y, s, size=10, weight="normal", anchor="middle", fill=None):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{F_SANS}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}" fill="{fill or S.PAL["ink"]}">{html.escape(s)}</text>')


def _rect(x, y, w, h, role, emph=False):
    sw = S.LW["emphasis"] if emph else S.LW["control"]
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{S.TINT[role]}" '
            f'stroke="{S.ROLE[role]}" stroke-width="{sw}"/>')


def svg(state):
    st = STATES[state]; ch = set(st.get("changed", ())); o = []
    o.append(_t(PAD, 18, f"Test pyramid, {st['version']}", 11, weight="bold", anchor="start"))
    cx, bh, gap, top = 152, 40, 6, 34
    widths = (250, 214, 178, 142, 106)
    ys = {}
    for i in range(5):                      # draw top (operational) first
        n = 5 - i; w = widths[n - 1]; y = top + i * (bh + gap); ys[n] = y
        name, freq, cost = st["rows"][n - 1]
        o.append(_rect(cx - w / 2, y, w, bh, ROLES[n - 1], emph=n in ch))
        o.append(_t(cx, y + 17, f"L{n} {name}", 10.5, weight="bold"))
        o.append(_t(cx, y + 32, freq, 9.5))
        o.append(_t(W - PAD, y + 25, cost, 10, anchor="end", weight="bold" if n in ch else "normal"))
    # merge gate spans L1 to L3 on the left
    y1, y3 = ys[1] + bh, ys[3]
    gx = 14
    sw = S.LW["emphasis"] if "gate" in ch else S.LW["control"]
    o.append(f'<line x1="{gx}" y1="{y3:.1f}" x2="{gx}" y2="{y1:.1f}" stroke="{S.ROLE["blocker"]}" stroke-width="{sw}"/>')
    for yy in (y3, y1):
        o.append(f'<line x1="{gx}" y1="{yy:.1f}" x2="{gx + 8}" y2="{yy:.1f}" stroke="{S.ROLE["blocker"]}" stroke-width="{sw}"/>')
    yb = ys[1] + bh + 22
    o.append(_t(PAD, yb, st["foot"], 10, weight="bold", anchor="start", fill=S.PAL["ink"]))
    o.append(_t(W - PAD, top - 6, "cost per run", 9.5, anchor="end"))
    H = yb + 12
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}pt" height="{H}pt" viewBox="0 0 {W} {H}">'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>' + "".join(o) + "</svg>")


def render(state, stem, source):
    return fde_svg.render_svg(svg(state), stem, kind="diagram", source=source, tool="hand-laid SVG (signature12.py)",
                              data=f"signature12.STATES['{state}']")
