"""Turn a week of calendar, tickets and commits into a time-allocation table.

Hours come only from the calendar (focus blocks included), so nothing is counted twice. Tickets and
commits are counted as evidence of what the hours served, not as hours. Every entry is filed under
one of the six verbs of the job (discover, decide, access, build, pass, hand over) or under internal
or travel. Customer contact is any calendar hour with someone from the customer's domain in the room.

The verdict is deterministic. No model is called anywhere in this lab.
"""
import csv, pathlib, sys
from dataclasses import dataclass, field

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "fieldkit"))
from fieldkit.fixtures import CUSTOMERS, caldwell_tracker  # noqa: E402

VERBS = ("discover", "decide", "access", "build", "pass", "hand over")
BUCKETS = VERBS + ("internal", "travel")
PATH_VERB = [("evals/", "pass"), ("docs/status/", "pass"), ("docs/decisions/", "decide"),
             ("docs/runbook/", "hand over"), ("ops/", "access")]          # anything else is build
MIN_CONTACT_SHARE = 0.15


def hours(start, end):
    h1, m1 = map(int, start.split(":")); h2, m2 = map(int, end.split(":"))
    return (h2 * 60 + m2 - h1 * 60 - m1) / 60


def commit_verb(path):
    return next((v for prefix, v in PATH_VERB if path.startswith(prefix)), "build")


@dataclass
class Week:
    name: str
    days: tuple
    hours: dict = field(default_factory=lambda: {b: 0.0 for b in BUCKETS})
    contact: dict = field(default_factory=lambda: {b: 0.0 for b in BUCKETS})
    commits: dict = field(default_factory=lambda: {b: 0 for b in BUCKETS})
    tickets_closed: int = 0
    customer_items_moved: list = field(default_factory=list)
    access_days: set = field(default_factory=set)


def load(data_dir, name, customer_domains):
    if isinstance(customer_domains, str):
        customer_domains = (customer_domains,)
    d = pathlib.Path(data_dir)
    cal = list(csv.DictReader(open(d / f"{name}_calendar.csv")))
    days = tuple(sorted({int(r["day"]) for r in cal}))
    w = Week(name, days)
    for r in cal:
        tag, h = r["tag"], hours(r["start"], r["end"])
        if tag not in BUCKETS:
            raise ValueError(f"{name}: unknown tag {tag!r} on {r['title']!r}")
        w.hours[tag] += h
        if any("@" + dom in r["attendees"] for dom in customer_domains):
            w.contact[tag] += h
            if tag == "decide":
                w.customer_items_moved.append(f"day {r['day']} decision meeting: {r['title']}")
        if tag == "access":
            w.access_days.add(int(r["day"]))
    for r in csv.DictReader(open(d / f"{name}_tickets.csv")):
        opened = int(r["opened_day"]); closed = int(r["closed_day"]) if r["closed_day"] else None
        if closed is not None and days[0] <= closed <= days[-1]:
            w.tickets_closed += 1
        moved = days[0] <= opened <= days[-1] or (closed is not None and days[0] <= closed <= days[-1])
        if moved and r["owner"].split("@")[1] in customer_domains:
            w.customer_items_moved.append(f"{r['id']} ({r['owner'].split('@')[0]}): {r['title']}")
    for line in open(d / f"{name}_commits.log"):
        _h, day, _a, _s, path = line.rstrip("\n").split("|")
        v = commit_verb(path)
        w.commits[v] += 1
        if v == "access":
            w.access_days.add(int(day.split()[1]))
    return w


def rotation_days(days, tracker=None):
    """Days in this week on which the model gateway key rotates (from fieldkit's access tracker)."""
    if tracker is None:
        return []
    key = tracker.requests.get("gateway-key")
    if key is None:
        return []
    return [d for d in days if key.next_expiry(d - 1) == d]


def verdict(w, baseline=None, tracker=None):
    total = sum(w.hours.values()); contact = sum(w.contact.values())
    share = contact / total if total else 0.0
    flags = []
    if share < MIN_CONTACT_SHARE:
        flags.append(f"customer contact {share:.0%} is below {MIN_CONTACT_SHARE:.0%}")
    if not w.customer_items_moved:
        flags.append("nothing the customer owns moved this week")
    untouched = [v for v in VERBS if w.hours[v] == 0 and w.commits[v] == 0]
    if untouched:
        flags.append("verbs untouched: " + ", ".join(untouched))
    missed = [d for d in rotation_days(w.days, tracker) if d not in w.access_days]
    if missed:
        flags.append("gateway key rotated on day " + ", ".join(map(str, missed)) + " with no check recorded")
    output_up = baseline is not None and sum(w.commits.values()) >= 1.5 * sum(baseline.commits.values())
    if output_up and share < MIN_CONTACT_SHARE and not w.customer_items_moved:
        label = "PRODUCTIVE-LOOKING: output up, nothing the customer owns moved"
    elif flags:
        label = "CHECK"
    else:
        label = "OK"
    return share, flags, label


def table(w, customer):
    total = sum(w.hours.values()); contact = sum(w.contact.values())
    lines = [f"TIME ALLOCATION  {w.name}  {customer['name']} ({customer['city']}, {customer['cloud']})  "
             f"days {w.days[0]}-{w.days[-1]}",
             f"{'bucket':<11}{'hours':>7}{'share':>7}{'with customer':>15}{'commits':>9}"]
    for b in BUCKETS:
        lines.append(f"{b:<11}{w.hours[b]:>7.1f}{w.hours[b] / total:>7.0%}{w.contact[b]:>15.1f}{w.commits[b]:>9}")
    lines.append(f"{'total':<11}{total:>7.1f}{1:>7.0%}{contact:>15.1f}{sum(w.commits.values()):>9}")
    lines.append(f"tickets closed: {w.tickets_closed}   customer-owned items moved: {len(w.customer_items_moved)}")
    for item in w.customer_items_moved:
        lines.append(f"  - {item}")
    return "\n".join(lines)


def compare(a, b):
    rows = [("calendar hours", sum(a.hours.values()), sum(b.hours.values())),
            ("hours with customer", sum(a.contact.values()), sum(b.contact.values())),
            ("commits", sum(a.commits.values()), sum(b.commits.values())),
            ("tickets closed", a.tickets_closed, b.tickets_closed),
            ("customer-owned items moved", len(a.customer_items_moved), len(b.customer_items_moved)),
            ("verbs touched (of 6)", sum(1 for v in VERBS if a.hours[v] or a.commits[v]),
             sum(1 for v in VERBS if b.hours[v] or b.commits[v]))]
    lines = [f"{'measure':<28}{a.name:>18}{b.name:>18}"]
    for label, x, y in rows:
        fmt = (lambda v: f"{v:>18.1f}") if isinstance(x, float) else (lambda v: f"{v:>18}")
        lines.append(f"{label:<28}{fmt(x)}{fmt(y)}")
    return "\n".join(lines)


def report(w, customer, baseline=None, tracker=None):
    share, flags, label = verdict(w, baseline, tracker)
    out = [table(w, customer), f"customer-contact share: {share:.0%}"]
    out += [f"flag: {f}" for f in flags] or ["flag: none"]
    out.append(f"verdict: {label}")
    return "\n".join(out)


if __name__ == "__main__":
    here = pathlib.Path(__file__).resolve().parent
    cust = CUSTOMERS["caldwell"]
    a = load(here / "data", "week_a_caldwell", "caldwellmutual.com")
    b = load(here / "data", "week_b_injected", "caldwellmutual.com")
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("a", "all"):
        print(report(a, cust, tracker=caldwell_tracker())); print()
    if which in ("b", "all"):
        print(report(b, cust, baseline=a, tracker=caldwell_tracker())); print()
    if which in ("compare", "all"):
        print(compare(a, b)); print()
    if which in ("greystone", "all"):
        g = CUSTOMERS["greystone"]
        naive = load(here / "data", "week_c_greystone", "greystonehealth.org")
        naive.name = "week_c_one_domain"
        print(report(naive, g)); print()
        full = load(here / "data", "week_c_greystone", ("greystonehealth.org", "greystone-msp.net"))
        full.name = "week_c_all_domains"
        print(report(full, g))
