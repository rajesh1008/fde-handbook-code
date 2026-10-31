"""Signature 10: the lineage chain for one output, hand-laid SVG (BOOK-PROMPT rev 003.1, Part C; Part A figure rules 1 and 4).
source document -> page -> extraction method -> calculation -> claim -> release, with the reference table the
calculation cites drawn beside it. One template for every recurrence: identical layout and palette; only the data
changes. A broken state draws the failing link in the blocker color at the emphasis stroke (2.5 pt), dashed.
A chapter adds its state to STATES (in its own figure script, as Signatures 6 and 7 do) and calls render().

State: dict(details=[6 strings], side=[6 strings or ""], ref=(line1, line2), broken=bool, note=str or "").
"""
import sys, pathlib, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "05-build/design"))
import matplotlib.colors as mc
import fde_style as S, fde_svg

W = 396; PAD = 10; BW = 178; BH = 38; GAP = 20; TOP = 14
KINDS = ("source document", "page", "extraction method", "calculation", "claim", "release")
ROLES = ("data", "data", "model", "system", "evidence", "approval")
RX, RW = 262, 124
F_SANS = "Source Sans Pro"
STATES = {}


def _t(x, y, s, size=10, weight="normal", anchor="start", fill=None):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{F_SANS}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}" fill="{fill or S.PAL["ink"]}">{html.escape(s)}</text>')


def _rect(x, y, w, h, role, lw=None, dash=False):
    fill = mc.to_hex(S.TINT[role])
    d = ' stroke-dasharray="5,3"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" fill="{fill}" stroke="{S.ROLE[role]}" '
            f'stroke-width="{lw or S.LW["control"]}"{d}/>')


def _arrow_down(x, y1, y2):
    return (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2 - 6}" stroke="{S.PAL["ink"]}" stroke-width="{S.LW["control"]}"/>'
            f'<polygon points="{x - 4},{y2 - 7} {x + 4},{y2 - 7} {x},{y2}" fill="{S.PAL["ink"]}"/>')


def svg(state):
    st = STATES[state]; o = []
    for i, (k, role) in enumerate(zip(KINDS, ROLES)):
        y = TOP + i * (BH + GAP)
        o.append(_rect(PAD, y, BW, BH, role))
        o.append(_t(PAD + 8, y + 15, k, 10, weight="bold"))
        o.append(_t(PAD + 8, y + 30, st["details"][i], 10))
        if st["side"][i]:
            o.append(_t(PAD + BW + 12, y + 23, st["side"][i], 10))
        if i < len(KINDS) - 1:
            o.append(_arrow_down(PAD + BW / 2, y + BH, y + BH + GAP))
    y = TOP + 3 * (BH + GAP)
    broken = st["broken"]
    role = "blocker" if broken else "approval"
    o.append(_rect(RX, y, RW, BH, role, lw=S.LW["emphasis"] if broken else None, dash=broken))
    o.append(_t(RX + 8, y + 15, st["ref"][0], 10, weight="bold"))
    o.append(_t(RX + 8, y + 30, st["ref"][1], 10))
    x1, x2, ym = PAD + BW, RX, y + BH / 2
    o.append(f'<line x1="{x1}" y1="{ym}" x2="{x2}" y2="{ym}" stroke="{S.ROLE[role]}" '
             f'stroke-width="{S.LW["emphasis"] if broken else S.LW["control"]}"{" stroke-dasharray=\"5,3\"" if broken else ""}/>')
    if broken:
        cx = (x1 + x2) / 2
        for a, b in ((-7, 7), (7, -7)):
            o.append(f'<line x1="{cx + a}" y1="{ym - 7}" x2="{cx + b}" y2="{ym + 7}" stroke="{S.ROLE["blocker"]}" stroke-width="{S.LW["emphasis"]}"/>')
    if st.get("note"):
        o.append(_t(RX, y + BH + 16, st["note"], 10, weight="bold", fill=S.PAL["ink"]))
    H = TOP + 6 * BH + 5 * GAP + 14
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}pt" height="{H:.0f}pt" viewBox="0 0 {W} {H:.0f}">'
            f'<rect x="0" y="0" width="{W}" height="{H:.0f}" fill="#FFFFFF"/>' + "".join(o) + "</svg>")


def render(state, stem, source):
    return fde_svg.render_svg(svg(state), stem, kind="diagram", source=source, tool="hand-laid SVG (signature10.py)",
                              data=f"signature10.STATES['{state}']")
