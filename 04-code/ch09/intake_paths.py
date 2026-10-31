"""Listing 9.2: Caldwell's eleven intake paths (Chapter 6, Table 6.3) walked through the 12-step pipeline.

Each path enters the same pipeline; what changes is which steps run and where the received date comes from.
Volumes are the day-26 monthly counts from Chapter 6. P09 carries an extra step that the tree refuses.
"""
import _path  # noqa: F401
from fieldkit.autonomy import Step, TreeError, walk, SHORT
from pipelines import CALDWELL

BY_N = {s.n: s for s in CALDWELL}
ALL = [s.n for s in CALDWELL]

# path, door, documents a month, steps skipped, where C02 reads the received date, note
PATHS = [
    ("P01", "paper mail, Hartford mailroom", 4100, (), "envelope date stamp", ""),
    ("P02", "main claims fax line", 2300, (), "fax header", ""),
    ("P03", "claims shared mailbox", 2900, (), "mail header", ""),
    ("P04", "agent portal upload", 2450, ("C06",), "upload timestamp", "agent picks the type from a closed list"),
    ("P05", "closed Springfield fax, forwarded", 610, (), "original fax header, not the forward", ""),
    ("P06", "email to an adjuster, forwarded", 540, (), "original message date, not the forward", ""),
    ("P07", "phone report, papers follow by mail", 980, (), "envelope date stamp", "C05 always finds the claim"),
    ("P08", "administrator's nightly file transfer", 420, ("C06", "C07", "C11"), "file record date",
     "structured records: type, code and notes arrive as fields"),
    ("P09", "mail routed through the finance cage", 160, (), "envelope date stamp",
     "finance decides whether the item is a claim"),
    ("P10", "attorney letters through legal", 230, ("C07", "C08", "C09", "C10", "C11"), "envelope date stamp",
     "C06 marks out of scope; legal coordinator queue"),
    ("P11", "repair-estimate platform email", 110, ("C06",), "platform submission time",
     "sender rule fixes the type"),
]

# The step only P09 has. Tom Whitfield described it; nobody owns a written rule for it (Chapter 6, day 19).
P09_EXTRA = Step("C00", "finance decides whether a check-bearing item is a claim", written_rules=True, rule_owner=None)


def steps_for(path_id):
    row = next(p for p in PATHS if p[0] == path_id)
    return [BY_N[n] for n in ALL if n not in row[3]]


def walk_paths(p09_owner=None):
    """Yield (path row, steps, counts by class, refusal text or None)."""
    for row in PATHS:
        steps = steps_for(row[0])
        refusal = None
        if row[0] == "P09":
            extra = Step(P09_EXTRA.n, P09_EXTRA.name, written_rules=True, rule_owner=p09_owner)
            try:
                walk(extra)
                steps = [extra] + steps
            except TreeError as e:
                refusal = str(e)
        counts = [0, 0, 0, 0]
        for s in steps:
            counts[walk(s)[0]] += 1
        yield row, steps, counts, refusal


if __name__ == "__main__":
    print(f"{'path':<5}{'door':<40}{'docs/mo':>8} {'steps':>5} {'det':>4}{'rul':>4}{'sml':>4}{'frn':>4}  received date from")
    vol = model_calls = 0; frontier_docs = 0
    for row, steps, c, refusal in walk_paths():
        vol += row[2]; model_calls += row[2] * (c[2] + c[3]); frontier_docs += row[2] * c[3]
        print(f"{row[0]:<5}{row[1]:<40}{row[2]:>8,} {len(steps):>5} {c[0]:>4}{c[1]:>4}{c[2]:>4}{c[3]:>4}  {row[4]}")
        if refusal:
            print(f"      REFUSED  {refusal}")
    print(f"monthly documents {vol:,}; model calls per document {model_calls/vol:.2f}; "
          f"documents reaching the frontier step {frontier_docs/vol:.1%}")
    print("with an owner named for the finance rule:")
    for row, steps, c, refusal in walk_paths(p09_owner="Anne Kessler"):
        if row[0] == "P09":
            print(f"P09  steps {len(steps)}  det {c[0]} rules {c[1]} small {c[2]} frontier {c[3]}  refusal: {refusal}")
