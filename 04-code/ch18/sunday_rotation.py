"""Failure injection: the seven-day rotation on Sunday day 73, naive adapter against the fieldkit adapter.

Deterministic stand-in: one mirrored claim document every ten minutes from Saturday day 72 00:00 to
Monday day 74 12:00, three model calls per document, Caldwell-style rotation (Sunday 02:00, one-hour grace).
"""
import _paths  # noqa: F401
from fieldkit.gateway import GatewayAdapter, GatewayStop, RotationSchedule, cost_per_success, DAY
from gateway_sim import SimGateway, SecretStore, Clock, fmt, PRICES, PIPELINE
from naive_adapter import NaiveAdapter

START, END, STEP = 72 * DAY, 74 * DAY + 12 * 3600, 600
RESTART_AT = 74 * DAY + 9 * 3600 + 10 * 60     # Monday 09:10, when someone looks


def run(kind):
    clock, store = Clock(START), SecretStore()
    gw = SimGateway(clock, store, start_key=10)
    common = dict(app_id="nl-shadow", api_version="2025-04-01", clock=clock.now, sleep=clock.sleep,
                  source_ip="10.20.4.17")
    make = (lambda: NaiveAdapter(gw, store.read, **common)) if kind == "naive" else \
           (lambda: GatewayAdapter(gw, store.read, rotation=RotationSchedule(3, 2, 3600), prices=PRICES,
                                   expected_versions={"extract-standard": "extract-2026-01"}, **common))
    ad, up, consecutive = make(), True, 0
    events, scored, missed, filtered, docs = [], 0, 0, 0, 0
    first_fail = None
    for doc, t in enumerate(range(START, END, STEP)):
        docs += 1
        clock.t = max(clock.t, t)
        if not up:
            if t >= RESTART_AT:
                ad, up, consecutive = make(), True, 0
                events.append((t, "restarted by hand; key re-read at start"))
            else:
                missed += 1
                continue
        try:
            ok = True
            for dep in PIPELINE:
                res = ad.call(dep, {"doc": doc, "text": "claim"})
                if kind != "naive" and res[0].kind == "content_filtered":
                    filtered += 1; ok = False
                    break
            scored += ok
            consecutive = 0
        except (RuntimeError, GatewayStop) as e:
            missed += 1; consecutive += 1
            if "content_filter" in str(e):
                consecutive = 0
                continue
            first_fail = first_fail or t
            events.append((t, f"document failed: {str(e)[:48]}"))
            if consecutive >= 3:
                up = False
                events.append((t, "runner exited after 3 consecutive failures (no restart policy)"))
    return gw, ad, events, docs, scored, missed, filtered, first_fail


for kind in ("naive", "fieldkit"):
    gw, ad, events, docs, scored, missed, filtered, ff = run(kind)
    print(f"== {kind} adapter ==")
    print(f"rotations: {', '.join(fmt(r) for r in gw.rotations)}; old key valid one hour after")
    for t, e in events[:6]:
        print(f"  {fmt(t)}  {e}")
    if kind == "fieldkit":
        for t, why in ad.refreshes:
            print(f"  {fmt(t)}  key read ({why})")
    stops = [t for t, e in events if "exited" in e]
    starts = [t for t, e in events if "restarted" in e]
    if stops and starts:
        d = starts[0] - ff
        print(f"  shadow runner down from {fmt(ff)} to {fmt(starts[0])}: {d // 3600} h {d % 3600 // 60} min")
    print(f"documents mirrored {docs}, scored {scored}, missed {missed}, routed to a person {filtered}")
    denied = sum(1 for (_, _, s) in gw.log if s == 401)
    print(f"gateway 401s {denied}; secret-store reads {gw.store.reads}")
    if kind == "fieldkit":
        total, per_call, per_doc = cost_per_success(ad.records, scored)
        calls = sum(1 for r in ad.records if r.kind == "ok")
        print(f"cost (stand-in rates, USD): total {total:.2f}, per successful call {per_call:.4f}, "
              f"per scored document {per_doc:.4f} over {calls} calls")
    print()
