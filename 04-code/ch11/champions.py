"""Champion register: who already wants this, what they can and cannot do, and every ask made of them."""
from dataclasses import dataclass, field

ALLOWED = ("introduce", "explain", "test", "relay")      # what a champion can be asked for
BYPASS = ("approve", "decide", "override")               # what belongs to an approver or owner, never a champion
IDLE_AFTER = 21


@dataclass
class Ask:
    day: int
    text: str
    kind: str
    belongs_to: str = ""        # for bypass kinds: who actually holds the decision


@dataclass
class Champion:
    key: str
    name: str
    why: str                    # why this person already wants it, in their words
    can: tuple
    cannot: tuple
    asks: list = field(default_factory=list)


def check_register(champs, today):
    out = []
    for c in champs:
        if not c.cannot:
            out.append(("WARN", "no-limits", f"{c.name}: no written limits; a champion with none gets asked for anything"))
        for a in c.asks:
            if a.kind in BYPASS:
                out.append(("BLOCK", "bypass", f"day {a.day}: asked {c.name} to {a.text}; that is {a.belongs_to}'s call"))
            elif a.kind not in ALLOWED:
                out.append(("WARN", "unknown-ask", f"day {a.day}: '{a.kind}' is not a recognized ask"))
        last = max((a.day for a in c.asks), default=None)
        if last is None or today - last > IDLE_AFTER:
            out.append(("WARN", "idle", f"{c.name}: no ask in {IDLE_AFTER} days; champions who are not used drift"))
    return out


def register_report(champs, today):
    lines = [f"Champion register, day {today}: {len(champs)} champions"]
    for c in champs:
        lines.append(f"  {c.name}: wants it because {c.why}")
        lines.append(f"    can:    {'; '.join(c.can)}")
        lines.append(f"    cannot: {'; '.join(c.cannot) or '(not written)'}")
        for a in c.asks:
            lines.append(f"    day {a.day:>2} {a.kind:<9} {a.text}")
    for lv, code, msg in check_register(champs, today):
        lines.append(f"  {lv:<5} {code:<8} {msg}")
    return "\n".join(lines)
