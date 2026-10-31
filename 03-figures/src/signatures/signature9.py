"""Signature 9: the surface-and-brain boundary, hand-laid SVG (BOOK-PROMPT rev 003.1, Part C; Part A figure rules 1 and 4).
Left zone: the surface where people already work (suite chat pane, the suite sign-in, the answer card). Right zone:
the governed cloud (mode flag, token broker, orchestrator, model behind the gateway, verifier, audit log) and the
sources. One request crosses the boundary per turn and one response comes back. One template for every recurrence:
identical layout and palette; only the labels and the broken link change. A broken state draws the failing link in
the blocker color at the emphasis stroke (2.5 pt), dashed, with a cross.
A chapter adds its state to STATES (in its own figure script) and calls render().

State: dict(zone=(left title, right title), surface=[3 labels], brain=dict(role->label), crossing=(request label,
response label), broken=None or "broker" or "boundary", note=str or "")."""
import sys, pathlib, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "05-build/design"))
import matplotlib.colors as mc
import fde_style as S, fde_svg

W, H = 396, 292
LX, LW_, RX1, RX2, BW, BH = 14, 104, 178, 290, 100, 34
ROWS = (46, 100, 154, 208)
F_SANS = "Source Sans Pro"
STATES = {
    "ch24": dict(zone=("suite: where they work", "governed cloud"),
                 surface=["suite chat pane", "suite sign-in", "answer card"],
                 brain=dict(flag="mode flag", broker="token broker", orch="orchestrator", model="model via gateway",
                            verify="verifier", audit="audit log", sources="six sources"),
                 crossing=("1 call per turn", "answer, sources"), broken=None, note=""),
}


def _t(x, y, s, size=10, weight="normal", anchor="start", fill=None):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{F_SANS}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}" fill="{fill or S.PAL["ink"]}">{html.escape(s)}</text>')


def _rect(x, y, w, h, role, lw=None, dash=False, label=""):
    fill = mc.to_hex(S.TINT[role]); d = ' stroke-dasharray="5,3"' if dash else ""
    r = (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" fill="{fill}" stroke="{S.ROLE[role]}" '
         f'stroke-width="{lw or S.LW["control"]}"{d}/>')
    return r + (_t(x + w / 2, y + h / 2 + 4, label, 10, "bold", "middle") if label else "")


def _arrow(x1, y1, x2, y2, color=None, lw=None, dash=False):
    import math
    c = color or S.PAL["ink"]; a = math.atan2(y2 - y1, x2 - x1); L = 7
    bx, by = x2 - L * math.cos(a), y2 - L * math.sin(a)
    px, py = 4 * math.sin(a), -4 * math.cos(a)
    d = ' stroke-dasharray="5,3"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{c}" stroke-width="{lw or S.LW["control"]}"{d}/>'
            f'<polygon points="{bx + px:.1f},{by + py:.1f} {bx - px:.1f},{by - py:.1f} {x2:.1f},{y2:.1f}" fill="{c}"/>')


def _cross(cx, cy):
    return "".join(f'<line x1="{cx + a}" y1="{cy - 7}" x2="{cx + b}" y2="{cy + 7}" stroke="{S.ROLE["blocker"]}" '
                   f'stroke-width="{S.LW["emphasis"]}"/>' for a, b in ((-7, 7), (7, -7)))


def svg(state):
    st = STATES[state]; b = st["brain"]; o = []; br = st["broken"]
    # zones and the boundary
    o.append(f'<rect x="6" y="8" width="120" height="{H - 46}" fill="#FFFFFF" stroke="{S.PAL["grey"]}" stroke-width="0.75"/>')
    o.append(f'<rect x="170" y="8" width="220" height="{H - 46}" fill="#FFFFFF" stroke="{S.PAL["grey"]}" stroke-width="0.75"/>')
    o.append(_t(66, 26, st["zone"][0], 10, "bold", "middle")); o.append(_t(280, 26, st["zone"][1], 10, "bold", "middle"))
    bc = S.ROLE["blocker"] if br == "boundary" else S.PAL["ink"]
    o.append(f'<line x1="148" y1="8" x2="148" y2="{H - 38}" stroke="{bc}" stroke-width="{S.LW["emphasis"]}" stroke-dasharray="2,3"/>')
    # surface
    for (y, lab, role) in zip((ROWS[0], ROWS[1], ROWS[3]), st["surface"], ("system", "approval", "system")):
        o.append(_rect(LX, y, LW_, BH, role, label=lab))
    # brain
    bro = br == "broker"
    o.append(_rect(RX1, ROWS[0], BW, BH, "approval", label=b["flag"]))
    o.append(_rect(RX1, ROWS[1], BW, BH, "approval" if not bro else "blocker", dash=bro,
                   lw=S.LW["emphasis"] if bro else None, label=b["broker"]))
    o.append(_rect(RX2, ROWS[1], BW, BH, "blocker" if bro else "data", label=b["sources"]))
    o.append(_rect(RX1, ROWS[2], BW, BH, "system", label=b["orch"]))
    o.append(_rect(RX2, ROWS[2], BW, BH, "model", label=b["model"]))
    o.append(_rect(RX1, ROWS[3], BW, BH, "evidence", label=b["verify"]))
    o.append(_rect(RX2, ROWS[3], BW, BH, "evidence", label=b["audit"]))
    # flows inside the brain
    cx = RX1 + BW / 2
    for y1, y2 in ((ROWS[0] + BH, ROWS[1]), (ROWS[1] + BH, ROWS[2]), (ROWS[2] + BH, ROWS[3])):
        o.append(_arrow(cx, y1, cx, y2))
    o.append(_arrow(RX1 + BW, ROWS[2] + BH / 2, RX2, ROWS[2] + BH / 2))
    o.append(_arrow(RX1 + BW, ROWS[3] + BH / 2, RX2, ROWS[3] + BH / 2))
    if bro:
        o.append(_arrow(RX1 + BW - 10, ROWS[2], RX2 + 10, ROWS[1] + BH, S.ROLE["blocker"], S.LW["emphasis"], True))
        o.append(_cross((RX1 + BW + RX2) / 2, (ROWS[2] + ROWS[1] + BH) / 2))
    else:
        o.append(_arrow(RX1 + BW, ROWS[1] + BH / 2, RX2, ROWS[1] + BH / 2))
    # the crossing: one request, one response
    o.append(_arrow(LX + LW_, ROWS[0] + BH / 2, RX1, ROWS[0] + BH / 2, bc, S.LW["emphasis"]))
    o.append(_arrow(RX1, ROWS[3] + BH / 2, LX + LW_, ROWS[3] + BH / 2, bc, S.LW["emphasis"]))
    o.append(_t(66, ROWS[0] - 6 + 0, "", 10))
    o.append(_t(LX, ROWS[2] + 8, st["crossing"][0], 10, "bold"))
    o.append(_t(LX, ROWS[2] + 24, st["crossing"][1], 10))
    if br == "boundary":
        o.append(_cross(148, ROWS[2] + BH / 2))
    if st.get("note"):
        o.append(_t(6, H - 14, st["note"], 10, "bold"))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}pt" height="{H}pt" viewBox="0 0 {W} {H}">'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>' + "".join(o) + "</svg>")


def render(state, stem, source):
    return fde_svg.render_svg(svg(state), stem, kind="diagram", source=source, tool="hand-laid SVG (signature9.py)",
                              data=f"signature9.STATES['{state}']")
