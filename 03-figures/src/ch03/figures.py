"""Chapter 3 figures 3.2 to 3.18, drafted to the 003.1 figure rules (Figure 3.1, Signature 7, is
fig03_01_signature7.py on the shared hand-laid SVG template).

Render (from the book root):
    /workspace/books/.venv/bin/python 05-build/tools/render_figures.py ch03
    (or: /workspace/books/.venv/bin/python 03-figures/src/ch03/figures.py)

Data: every plotted number is computed here from the Chapter 3 lab
(04-code/ch03: caldwell_docs.py, demo_extract.py, scoring.py); diagram labels
are terms the chapter uses. Outputs: Kindle PNGs in 03-figures/ch03/
(5.5 in printed width, 300 ppi, 1,650 px wide, sRGB, no alpha), print PDF and SVG
in 03-figures/ch03/print/ and manifests in 03-figures/ch03/manifest/, all written by
fde_style.save(), which refuses a figure that breaks a mechanical rule. Style:
03-figures/style.md and 03-figures/book.mplstyle, loaded with fde_style.use().

Look: palette roles only, plus two greys and black; Source Sans Pro for labels,
JetBrains Mono for identifiers; strokes 0.75 pt (data flow), 1.5 pt (control,
outlines), 2.5 pt (emphasis); one arrowhead; square corners; white background;
no transparency, shadows or gradients; text 9.5 pt or larger at printed width;
color meaning repeated by hatch, line style or label.
"""
import pathlib
import sys
from collections import Counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[3]
for p in ("04-code/fieldkit", "04-code/ch03", "05-build/design"):
    sys.path.insert(0, str(ROOT / p))
from caldwell_docs import FIELDS, caldwell_docs, demo_docs  # noqa: E402
from demo_extract import extract  # noqa: E402
from scoring import score  # noqa: E402
import fde_style as S  # noqa: E402

S.use()

PNG_DIR = ROOT / "03-figures" / "ch03"
PNG_DIR.mkdir(parents=True, exist_ok=True)

# palette (manual section 9 roles), two greys and black
ROLE = dict(model="#1F3A5F", system="#0F7C80", data="#D99A1E", evidence="#5A6F9C",
            blocker="#E05A47", approval="#3A8F4B", cost="#7B4B83")
HATCH = dict(model="", system="//", data="..", evidence="xx", blocker="\\\\", approval="", cost="--")
INK = "#1E2329"
GREY_D = "#5F6772"   # secondary text, ghost outlines (contrast 5.9:1 on white)
GREY_L = "#C9CED5"   # gridlines and rules only, never text
FLOW, CONTROL, EMPH = 0.75, 1.5, 2.5
FONT, MONO = "Source Sans Pro", "JetBrains Mono"
W = S.WIDTH_IN
DRAWN_AT = 5.4   # layouts were drafted at 5.4 in; canvas() keeps their y range
FS = 10

plt.rcParams.update({"svg.fonttype": "path"})   # everything else comes from book.mplstyle

CALD = score(caldwell_docs(), extract)
DEMO = score(demo_docs(), extract)


PLOTS = {6, 7, 8, 9, 15, 16, 18}


def save(fig, n):
    S.save(fig, f"fig03-{n:02d}", kind="plot" if n in PLOTS else "diagram", source=__file__,
           data="04-code/ch03 (Chapter 3 lab)" if n in (6, 7, 8, 9) else None)


def canvas(h):
    """Diagram canvas W x h inches; x runs 0-10, y runs 0-10*h/W (isotropic)."""
    fig = plt.figure(figsize=(W, h * W / DRAWN_AT), layout="none")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10 * h / DRAWN_AT)
    ax.axis("off")
    return fig, ax


def plot(h):
    fig, ax = plt.subplots(figsize=(W, h * W / DRAWN_AT), layout="constrained")
    return fig, ax


def box(ax, x, y, w, h, text="", role=None, fs=FS, mono=False, emph=False, ghost=False, tab=True,
        align="center"):
    """Square-cornered white box; a hatched role tab on the left carries the role in greyscale."""
    edge = GREY_D if ghost else (ROLE[role] if role else INK)
    ax.add_patch(Rectangle((x, y), w, h, facecolor="white", edgecolor=edge,
                           lw=EMPH if emph else CONTROL, ls=(0, (4, 2)) if ghost else "-", zorder=2))
    pad = 0.12
    if role and tab and not ghost:
        ax.add_patch(Rectangle((x, y), 0.22, h, facecolor=ROLE[role], edgecolor="white",
                               hatch=HATCH[role], lw=0, zorder=3))
        pad = 0.34
    if text:
        if align == "left":
            ax.text(x + pad, y + h / 2, text, ha="left", va="center", fontsize=fs,
                    family=MONO if mono else FONT, color=GREY_D if ghost else INK, zorder=4,
                    linespacing=1.25)
        else:
            cx = x + (pad - 0.12) / 2 + w / 2
            ax.text(cx, y + h / 2, text, ha="center", va="center", fontsize=fs,
                    family=MONO if mono else FONT, color=GREY_D if ghost else INK, zorder=4,
                    linespacing=1.2)


def arrow(ax, x1, y1, x2, y2, lw=FLOW, color=INK, ls="-"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), zorder=5,
                arrowprops=dict(arrowstyle="-|>", mutation_scale=11, color=color, lw=lw,
                                linestyle=ls, shrinkA=0, shrinkB=0))


def note(ax, x, y, text, fs=FS, color=INK, ha="left", weight="normal", mono=False):
    ax.text(x, y, text, fontsize=fs, color=color, ha=ha, va="center", weight=weight,
            family=MONO if mono else FONT, zorder=6, linespacing=1.2)


# 2. The week at a glance --------------------------------------------------------------------------------------
def f02():
    fig, ax = canvas(5.6)          # y 0..10.37
    note(ax, 2.0, 9.9, "what we did", weight="bold")
    note(ax, 6.2, 9.9, "what Caldwell saw", weight="bold")
    rows = [("kickoff, four promises", "a listening vendor", "approval"),
            ("demo, ten documents", "58% on its own mail", "blocker"),
            ("\u201call claims data\u201d", "a request with no owner", "blocker"),
            ("architecture review", "data outside the estate", "blocker"),
            ("typed deck", "\u201cgreen\u201d, unsupported", "blocker")]
    for k, (a, b, role) in enumerate(rows):
        y = 8.1 - k * 1.95
        note(ax, 0.1, y + 0.7, f"day {k + 1}", weight="bold")
        box(ax, 2.0, y, 3.9, 1.4, a, "model")
        box(ax, 6.2, y, 3.7, 1.4, b, role)
        arrow(ax, 5.9, y + 0.7, 6.18, y + 0.7)
    save(fig, 2)


# 3. Kickoff promises and who could verify them ------------------------------------------------------------------
def f03():
    fig, ax = canvas(5.0)          # y 0..9.26
    note(ax, 0.1, 8.85, "promise, day 1", weight="bold")
    note(ax, 6.3, 8.85, "who could check it", weight="bold")
    proms = ["accuracy above 95%", "live in under five months", "no integration work", "works on any document"]
    ys = [7.0, 5.2, 3.4, 1.6]
    for t, y in zip(proms, ys):
        box(ax, 0.1, y, 4.4, 1.2, t, "cost")
    box(ax, 6.3, 5.6, 3.6, 2.2, "nobody:\nno gold set,\nno gate dates", "blocker", emph=True)
    box(ax, 6.3, 3.4, 3.6, 1.2, "Priya Natarajan", "system")
    box(ax, 6.3, 1.6, 3.6, 1.2, "Anne Kessler", "system")
    for y, ty in ((7.6, 7.1), (5.8, 6.3), (4.0, 4.0), (2.2, 2.2)):
        arrow(ax, 4.5, y, 6.28, ty, lw=CONTROL)
    note(ax, 6.3, 0.75, "verifier in the record: none", color=INK)
    save(fig, 3)


# 4. Who was in the kickoff room -------------------------------------------------------------------------------
def f04():
    fig, ax = canvas(5.0)          # y 0..9.26
    ax.add_patch(Rectangle((0.1, 2.6), 9.8, 6.5, facecolor="white", edgecolor=INK, lw=CONTROL))
    note(ax, 0.35, 8.65, "kickoff room, sixth floor", weight="bold")
    note(ax, 0.35, 7.85, "Northlight", color=GREY_D)
    note(ax, 5.25, 7.85, "Caldwell Mutual", color=GREY_D)
    box(ax, 0.35, 5.9, 4.4, 1.4, "Graham Lowell\nVP Sales", "cost")
    box(ax, 0.35, 3.0, 4.4, 1.4, "the FDE", "model")
    box(ax, 5.25, 6.1, 4.4, 1.2, "Daniel Reyes\nCTO", "system")
    box(ax, 5.25, 4.55, 4.4, 1.2, "Anne Kessler\nHead of Claims", "system")
    box(ax, 5.25, 3.0, 4.4, 1.2, "Priya Natarajan\nenterprise architect", "system")
    note(ax, 0.1, 1.95, "not in the room", weight="bold", color=GREY_D)
    box(ax, 0.1, 0.25, 4.6, 1.3, "Laura Finch\nHead of FDE", ghost=True)
    box(ax, 5.3, 0.25, 4.6, 1.3, "Tom Whitfield\nwould use it", ghost=True, emph=True)
    save(fig, 4)


# 5. The day-2 data path ---------------------------------------------------------------------------------------------
def f05():
    fig, ax = canvas(5.6)          # y 0..10.37
    ax.add_patch(Rectangle((0.1, 5.7), 9.8, 4.5, facecolor="white", edgecolor=ROLE["system"], lw=CONTROL))
    ax.add_patch(Rectangle((0.1, 5.7), 9.8, 0.22, facecolor=ROLE["system"], edgecolor="white",
                           hatch=HATCH["system"], lw=0))
    note(ax, 0.35, 9.75, "Caldwell's estate", weight="bold")
    box(ax, 0.35, 7.6, 4.2, 1.4, "intake:\nmail, fax, email", "data")
    box(ax, 5.45, 7.6, 4.2, 1.4, "Kessler's mailbox", "data")
    arrow(ax, 4.55, 8.3, 5.43, 8.3)
    box(ax, 0.35, 6.2, 4.2, 1.0, "model gateway: unused", ghost=True)
    note(ax, 0.1, 5.2, "outside Caldwell's control", weight="bold")
    box(ax, 5.45, 3.4, 4.2, 1.3, "Northlight mailbox", "blocker")
    box(ax, 0.35, 3.4, 4.2, 1.3, "laptop notebook", "blocker")
    box(ax, 0.35, 0.4, 4.2, 1.3, "team chat:\ntwo screenshots", "blocker")
    box(ax, 5.45, 0.4, 4.2, 1.3, "model provider,\nNorthlight's key", "model")
    arrow(ax, 7.55, 7.6, 7.55, 4.72, lw=EMPH, color=ROLE["blocker"])
    note(ax, 7.75, 6.3, "boundary\ncrossed", fs=FS)
    arrow(ax, 5.45, 4.05, 4.57, 4.05)
    arrow(ax, 2.45, 3.4, 2.45, 1.72)
    arrow(ax, 4.0, 3.4, 5.6, 1.72)
    save(fig, 5)


# 6. Field accuracy, demo set against Caldwell's ten ---------------------------------------------------------------------
def f06():
    fig, ax = plot(5.6)
    a = [sum(r["ok"] for r in DEMO if r["field"] == f) * 10 for f in FIELDS]
    b = [sum(r["ok"] for r in CALD if r["field"] == f) * 10 for f in FIELDS]
    y = list(range(len(FIELDS)))
    ax.barh([i - 0.2 for i in y], a, 0.38, color="white", edgecolor=ROLE["evidence"], hatch="xx", lw=FLOW)
    ax.barh([i + 0.2 for i in y], b, 0.38, color=ROLE["data"], edgecolor="white", hatch="..", lw=0)
    for i, v in enumerate(b):
        ax.text(v + 1.5, i + 0.2, f"{v}%", va="center", fontsize=9.5)
    ax.text(101.5, -0.2, "demo set", va="center", fontsize=9.5)
    ax.text(b[0] + 11, 0.2, "Caldwell", va="center", fontsize=9.5)
    ax.set_yticks(y)
    ax.set_yticklabels([f.replace("_", " ") for f in FIELDS])
    ax.invert_yaxis()
    ax.set_xlim(0, 125)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel("fields correct, % of ten documents")
    ax.tick_params(axis="y", length=0)
    save(fig, 6)


# 7. Accuracy by intake channel -----------------------------------------------------------------------------------------
def f07():
    fig, ax = plot(4.6)
    chans = ["email", "fax", "mail"]
    n = {"email": 4, "fax": 3, "mail": 3}
    allf, nodef = [], []
    for ch in chans:
        rows = [r for r in CALD if r["channel"] == ch]
        allf.append(100 * sum(r["ok"] for r in rows) / len(rows))
        k = [r for r in rows if r["field"] not in ("date_received", "intake_channel")]
        nodef.append(100 * sum(r["ok"] for r in k) / len(k))
    y = [0, 1.2, 2.4]
    ax.barh([v - 0.2 for v in y], allf, 0.36, color=ROLE["data"], edgecolor="white", hatch="..", lw=0)
    ax.barh([v + 0.2 for v in y], nodef, 0.36, color="white", edgecolor=ROLE["evidence"], hatch="xx", lw=FLOW)
    for i, v in enumerate(y):
        ax.text(allf[i] + 1.5, v - 0.2, f"{allf[i]:.0f}%" + ("  all ten fields" if i == 0 else ""),
                va="center", fontsize=9.5)
        ax.text(nodef[i] + 1.5, v + 0.2, f"{nodef[i]:.0f}%" + ("  without the two\n        definition fields"
                                                               if i == 0 else ""), va="center", fontsize=9.5)
    ax.axvline(95, color=ROLE["cost"], ls=(0, (4, 2)), lw=CONTROL)
    ax.text(95, -0.5, "promised 95%", ha="center", fontsize=9.5)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{c} ({n[c]})" for c in chans])
    ax.invert_yaxis()
    ax.set_xlim(0, 135)
    ax.set_ylim(2.85, -0.75)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel("fields correct, %")
    ax.tick_params(axis="y", length=0)
    save(fig, 7)


# 8. Per-document, per-field correctness ---------------------------------------------------------------------------------
def f08():
    fig, ax = plot(5.6)
    docs = [d["id"] for d in caldwell_docs()]
    chan = {d["id"]: d["channel"] for d in caldwell_docs()}
    ok = {(r["doc"], r["field"]): r["ok"] for r in CALD}
    for i, d in enumerate(docs):
        for j, f in enumerate(FIELDS):
            good = ok[(d, f)]
            ax.add_patch(Rectangle((j + 0.04, i + 0.04), 0.92, 0.92,
                                   facecolor="white" if good else ROLE["blocker"],
                                   edgecolor=GREY_L if good else "white", hatch="" if good else "\\\\",
                                   lw=FLOW if good else 0))
            if not good:
                ax.text(j + 0.5, i + 0.5, "x", ha="center", va="center", fontsize=10, color=INK, weight="bold")
    ax.set_xlim(0, 10)
    ax.set_ylim(10, 0)
    ax.set_aspect("equal")
    ax.xaxis.tick_top()
    ax.set_xticks([j + 0.5 for j in range(10)])
    ax.set_xticklabels([f.replace("_", " ") for f in FIELDS], rotation=90, fontsize=9.5)
    ax.set_yticks([i + 0.5 for i in range(10)])
    ax.set_yticklabels([f"{d} {chan[d]}" for d in docs], fontsize=9.5)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xlabel("x = corrected by Anne Kessler", fontsize=9.5)
    save(fig, 8)


# 9. Corrections by cause, with the chapters that remove each cause -----------------------------------------------------
def f09():
    fig, ax = plot(4.4)
    fixes = {"definition: Caldwell's meaning differs": ("definition", "Ch 6, 8"),
             "scan text: layout or OCR noise": ("scan text", "Ch 9, 16"),
             "negation read as a mention": ("negation", "Ch 9, 26"),
             "phrasing the demo never saw": ("phrasing", "Ch 16, 26"),
             "vocabulary: demo words, not Caldwell codes": ("vocabulary", "Ch 7, 9"),
             "wrong person: sender or insured, not claimant": ("wrong person", "Ch 6"),
             "date convention": ("date convention", "Ch 9")}
    c = Counter(r["cause"] for r in CALD if not r["ok"]).most_common()
    ax.barh(range(len(c)), [n for _, n in c], 0.6, color=ROLE["blocker"], edgecolor="white", hatch="\\\\", lw=0)
    for i, (k, n) in enumerate(c):
        ax.text(n + 0.4, i, f"{n}   {fixes[k][1]}", va="center", fontsize=9.5)
    ax.set_yticks(range(len(c)))
    ax.set_yticklabels([fixes[k][0] for k, _ in c])
    ax.invert_yaxis()
    ax.set_xlim(0, 24)
    ax.set_xlabel(f"corrections, of {sum(n for _, n in c)}")
    ax.tick_params(axis="y", length=0)
    save(fig, 9)


# 10. The vague ask and the request that would have worked -----------------------------------------------------------
def f10():
    fig, ax = canvas(5.6)          # y 0..10.37
    note(ax, 0.1, 9.95, "day 3, as sent", weight="bold")
    box(ax, 0.1, 7.0, 9.8, 2.5, "subject: data for the pilot\nto:      Daniel Reyes\nowner:   none\ndue:     none",
        "blocker", mono=True, fs=9.5, align="left")
    note(ax, 0.1, 6.3, "as a tracked request", weight="bold")
    box(ax, 0.1, 1.4, 9.8, 4.4,
        "key:      claims-sample-200\nrung:     sampled\nowner:    Anne Kessler\nlocation: Caldwell sandbox\n"
        "readers:  two, named\ndelete:   day 90\nblocks:   accuracy claims", "evidence", mono=True, fs=9.5,
        align="left", emph=True)
    save(fig, 10)


# 11. The forward chain -------------------------------------------------------------------------------------------------
def f11():
    fig, ax = canvas(6.0)          # y 0..11.1
    hops = ["the FDE", "Daniel Reyes", "chief of staff", "data platform lead", "claims operations",
            "privacy office", "Priya Natarajan"]
    for i, h in enumerate(hops):
        y = 9.85 - i * 1.6
        last = i == len(hops) - 1
        box(ax, 2.2, y, 5.0, 1.0, h, "model" if i == 0 else "system", emph=last)
        if i:
            arrow(ax, 4.7, y + 1.6, 4.7, y + 1.02, lw=CONTROL)
            note(ax, 4.95, y + 1.3, str(i), fs=9.5, color=GREY_D)
    note(ax, 0.1, 10.35, "day 3", weight="bold")
    note(ax, 7.45, 0.75, "read on day 4,\nin the review", fs=FS)
    note(ax, 7.45, 5.9, "no owner,\nno due day,\nat any hop", fs=FS)
    save(fig, 11)


# 12. The three questions, answered as an architecture --------------------------------------------------------------
def f12():
    fig, ax = canvas(5.6)          # y 0..10.37
    ax.add_patch(Rectangle((0.1, 1.2), 7.0, 9.0, facecolor="white", edgecolor=ROLE["system"], lw=CONTROL))
    ax.add_patch(Rectangle((0.1, 1.2), 7.0, 0.22, facecolor=ROLE["system"], edgecolor="white",
                           hatch=HATCH["system"], lw=0))
    note(ax, 0.35, 9.75, "Caldwell's AWS account", weight="bold")
    box(ax, 0.5, 7.3, 6.2, 1.5, "Northlight code,\nnamed region and VPC", "approval")
    box(ax, 0.5, 5.0, 6.2, 1.2, "Caldwell service identity", "approval")
    box(ax, 0.5, 2.0, 2.8, 1.8, "model\ngateway", "system")
    box(ax, 3.9, 2.0, 2.8, 1.8, "log store,\nnamed readers", "evidence")
    arrow(ax, 3.6, 7.3, 3.6, 6.22, lw=CONTROL)
    arrow(ax, 1.9, 5.0, 1.9, 3.82, lw=CONTROL)
    arrow(ax, 5.3, 5.0, 5.3, 3.82, lw=FLOW)
    arrow(ax, 1.9, 2.0, 1.9, 0.25, lw=CONTROL)
    note(ax, 2.1, 0.6, "to the model provider", fs=9.5)
    for y, t in ((8.05, "where does\nit run?"), (5.6, "whose\nidentity?"), (2.9, "who sees\nthe logs?")):
        note(ax, 7.45, y, t, fs=FS, weight="bold")
        arrow(ax, 7.4, y, 6.75 if y > 3 else 6.75, y, lw=FLOW)
    save(fig, 12)


# 13. Every copy of the ten documents ---------------------------------------------------------------------------------
def f13():
    fig, ax = canvas(5.6)          # y 0..10.37
    note(ax, 0.1, 9.95, "inside Caldwell: kept", weight="bold")
    box(ax, 0.1, 8.3, 9.8, 1.1, "Kessler's sent email", "system")
    note(ax, 0.1, 7.55, "Northlight: deleted, attested", weight="bold")
    for k, t in enumerate(["Northlight mailbox", "laptop Downloads", "notebook outputs", "team chat screenshots"]):
        box(ax, 0.1 + (k % 2) * 5.0, 5.5 - (k // 2) * 1.5, 4.8, 1.1, t, "approval")
    note(ax, 0.1, 2.8, "model provider: not verifiable", weight="bold")
    box(ax, 0.1, 0.9, 9.8, 1.3, "request logs, deletion requested", "blocker", emph=True)
    save(fig, 13)


# 14. The day-5 deck as sent and the status the repository generates ----------------------------------------------------
def f14():
    fig, ax = canvas(5.8)          # y 0..10.74
    note(ax, 0.1, 10.3, "deck, typed", weight="bold")
    note(ax, 5.15, 10.3, "status, generated", weight="bold")
    sent = [("strong alignment", None), ("demo validated", "blocker"), ("98% accuracy", "blocker"),
            ("data next week", None), ("under five months", "blocker"), ("status: green", None)]
    gen = ["data on any rung: none", "blockers: 2", "open findings: 1", "58%, scored by Kessler",
           "decisions open: 4", "unverified promises: 4"]
    for k, ((t, role), g) in enumerate(zip(sent, gen)):
        y = 8.65 - k * 1.6
        box(ax, 0.1, y, 4.75, 1.15, t, role, ghost=role is None)
        box(ax, 5.15, y, 4.75, 1.15, g, "evidence")
    note(ax, 0.1, 0.45, "hatched: no Caldwell evidence; dashed: no claim", fs=9.5, color=GREY_D)
    save(fig, 14)


# 15. The baseline engagement: where eleven months go (illustrative shape) ----------------------------------------------
def f15():
    fig, ax = plot(4.6)
    phases = [("kickoff and demo", 0, 1, "cost"), ("waiting for access", 1, 4.5, "blocker"),
              ("security and architecture review", 3.5, 6.5, "evidence"), ("first real data, rework", 4.5, 7.5, "data"),
              ("model-risk review", 7, 9.5, "evidence"), ("shadow, then live", 9.5, 11, "approval")]
    for i, (t, a, b, role) in enumerate(phases):
        ax.barh(i, b - a, left=a, height=0.42, color=ROLE[role], edgecolor="white", hatch=HATCH[role], lw=0)
        ax.text(a, i - 0.3, t, va="bottom", fontsize=9.5,
                bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none"), zorder=4)
    ax.axvline(5, color=INK, ls=(0, (4, 2)), lw=CONTROL, zorder=1)
    ax.text(5.1, 5.75, "target: under 5", fontsize=9.5)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlim(0, 11.5)
    ax.set_ylim(6.0, -0.9)
    ax.set_xticks(range(0, 12))
    ax.set_xlabel("months from signature")
    save(fig, 15)


# 16. The baseline funnel (illustrative stage counts; 40 in 100 measured) -------------------------------------------------
def f16():
    fig, ax = plot(4.2)
    stages = [("signed", 100), ("reached real data", 82), ("passed security review", 71),
              ("passed model-risk review", 63), ("in production", 60)]
    for i, (t, v) in enumerate(stages):
        last = i == len(stages) - 1
        ax.barh(i, v, 0.55, color=ROLE["approval"] if last else "white",
                edgecolor="white" if last else ROLE["evidence"], hatch="" if last else "xx", lw=0 if last else FLOW)
        ax.text(v + 1.5, i, f"{v}", va="center", fontsize=9.5)
    ax.annotate("", xy=(100, 4.55), xytext=(60, 4.55),
                arrowprops=dict(arrowstyle="|-|", color=ROLE["blocker"], lw=EMPH, mutation_scale=4))
    ax.text(80, 4.8, "40 never reach production", ha="center", va="top", fontsize=9.5)
    ax.set_yticks(range(len(stages)))
    ax.set_yticklabels([t for t, _ in stages])
    ax.invert_yaxis()
    ax.set_xlim(0, 112)
    ax.set_ylim(5.5, -0.5)
    ax.set_xlabel("engagements, of 100 signed")
    ax.tick_params(axis="y", length=0)
    save(fig, 16)


# 17. The engagement repository on disk ---------------------------------------------------------------------------------
def f17():
    fig, ax = canvas(5.0)          # y 0..9.26
    tree = [("caldwell-repo/", None, ""), ("  ENGAGEMENT.md", None, "customer and layer"),
            ("  notes/", "data", "who said what"), ("  decisions/", "evidence", "owner, due day"),
            ("  access/", "blocker", "owner, blocks"), ("  evidence/", "approval", "scorer, documents"),
            ("  status/", "model", "generated")]
    for k, (t, role, w) in enumerate(tree):
        y = 8.6 - k * 1.2
        note(ax, 0.1, y, t, mono=True, fs=9.5)
        if role:
            box(ax, 4.6, y - 0.45, 5.3, 0.9, w, role)
        elif w:
            note(ax, 4.7, y, w, color=GREY_D)
    save(fig, 17)


# 18. What the week skipped, and the chapters that fix it -----------------------------------------------------------------
def f18():
    fig, ax = plot(4.6)
    rows = [("scoring rule, gold-set owner", [4, 8, 26]), ("real intake paths", [6]),
            ("named data owner", [15]), ("data inside the estate", [16, 17]),
            ("three written answers", [17]), ("calls through the gateway", [18]),
            ("rules before a model", [9]), ("generated status", [11, 13])]
    for i, (t, chs) in enumerate(rows):
        ax.plot([min(chs), max(chs)], [i, i], color=GREY_L, lw=CONTROL, zorder=1)
        ax.scatter(chs, [i] * len(chs), s=46, marker="s", color=ROLE["approval"], edgecolor=INK, lw=FLOW, zorder=2)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([t for t, _ in rows])
    ax.invert_yaxis()
    ax.set_xlim(2, 28)
    ax.set_xticks([4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26])
    ax.grid(axis="x", color=GREY_L, lw=FLOW)
    ax.set_axisbelow(True)
    ax.set_xlabel("chapter that fixes it")
    ax.tick_params(axis="y", length=0)
    save(fig, 18)


if __name__ == "__main__":
    for f in (f02, f03, f04, f05, f06, f07, f08, f09, f10, f11, f12, f13, f14, f15, f16, f17, f18):
        f()
    print("18 figures written")
