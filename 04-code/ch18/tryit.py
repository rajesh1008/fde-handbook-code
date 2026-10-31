"""Try It Yourself, Chapter 18. Run: python tryit.py a|b|c  (deterministic stand-in)."""
import sys
import _paths  # noqa: F401
from fieldkit.gateway import GatewayAdapter, RotationSchedule, DAY
from gateway_sim import SimGateway, SecretStore, Clock, fmt


def adapter(gw, store, clock, **kw):
    return GatewayAdapter(gw, store.read, app_id="nl-shadow", api_version="2025-04-01", clock=clock.now,
                          sleep=clock.sleep, source_ip="10.20.4.17", **kw)


def a():
    """Grace period 0 and no published schedule: does refresh-on-401 alone keep the runner up?"""
    for grace, sched in ((3600, False), (0, False), (0, True)):
        clock, store = Clock(72 * DAY), SecretStore()
        gw = SimGateway(clock, store, grace_s=grace)
        ad = adapter(gw, store, clock, rotation=RotationSchedule(3, 2, grace) if sched else None)
        retried = 0
        for t in range(72 * DAY, 75 * DAY, 600):
            clock.t = max(clock.t, t)
            rec, _ = ad.call("extract-standard", {"doc": t})
            retried += rec.attempts > 1
        print(f"grace {grace:>4} s, schedule known {str(sched):<5}: calls needing a second attempt {retried}, "
              f"gateway 401s {sum(1 for x in gw.log if x[2] == 401)}, all calls succeeded {all(r.kind == 'ok' for r in ad.records)}")


def b():
    """A backlog of 150 documents after an outage meets a 60-a-minute quota."""
    clock, store = Clock(74 * DAY + 9 * 3600), SecretStore()
    gw = SimGateway(clock, store, quota_per_min=60)
    ad = adapter(gw, store, clock, retry_budget=3)
    start = clock.t
    for doc in range(150):
        ad.call("extract-standard", {"doc": doc})
        clock.sleep(0)
    n429 = sum(1 for x in gw.log if x[2] == 429)
    print(f"150 calls, 429 responses {n429}, waits honored from Retry-After, elapsed {clock.t - start} s, "
          f"all succeeded {all(r.kind == 'ok' for r in ad.records)}")
    print("change quota_per_min to 20 and retry_budget to 1 to see which calls the adapter hands back")


def c():
    """30% of the alias's calls silently served by a smaller model: does the ledger see it?"""
    for report in (True, False):
        clock, store = Clock(80 * DAY), SecretStore()
        gw = SimGateway(clock, store, dilution=0.30, report_version=report)
        ad = adapter(gw, store, clock, expected_versions={"extract-standard": "extract-2026-01"})
        for k in range(500):
            clock.t = 80 * DAY + k * 60
            ad.call("extract-standard", {"doc": k})
        share = ad.versions.unexpected_share("extract-standard")
        top = ad.versions.counts["extract-standard"].most_common(3)
        print(f"version header sent {str(report):<5}: unexpected share {share:.2f}; served {top}")
    print("without the header the ledger can only say 'unreported'; a canary set with known answers is the fallback")


{"a": a, "b": b, "c": c}[sys.argv[1] if len(sys.argv) > 1 else "a"]()
