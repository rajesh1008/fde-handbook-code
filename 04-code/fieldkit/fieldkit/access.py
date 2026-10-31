"""Access tracker: every credential, network path and data release an engagement waits on.

The ladder is the order in which a deployment earns access to the customer's data:
synthetic -> sampled -> shadowed -> live. A request is never "in progress"; it is waiting on a named
person for a named next action, and the report says how many days it has waited.
"""
from dataclasses import dataclass, field
from typing import Optional

LADDER = ("synthetic", "sampled", "shadowed", "live")
STATUSES = ("not requested", "requested", "in review", "granted", "refused", "expired")


@dataclass
class AccessRequest:
    key: str
    what: str
    rung: str                      # the ladder rung this request opens
    owner: str                     # the customer-side person who can say yes
    requested_day: Optional[int]
    status: str = "requested"
    granted_day: Optional[int] = None
    next_action: str = ""
    blocks: list = field(default_factory=list)   # keys of work items this request blocks
    expires_every: Optional[int] = None          # days, for rotating credentials
    ball: str = "customer"                       # whose move it is: "customer" or "us" (v2)

    def __post_init__(self):
        if self.rung not in LADDER:
            raise ValueError(f"unknown rung {self.rung!r}")
        if self.status not in STATUSES:
            raise ValueError(f"unknown status {self.status!r}")

    def days_open(self, today: int) -> Optional[int]:
        if self.requested_day is None:
            return None
        end = self.granted_day if self.status == "granted" else today
        return end - self.requested_day

    def next_expiry(self, today: int) -> Optional[int]:
        if self.status != "granted" or not self.expires_every:
            return None
        cycles = (today - self.granted_day) // self.expires_every + 1
        return self.granted_day + cycles * self.expires_every


class AccessTracker:
    def __init__(self, customer: str, start_label: str = "day 0"):
        self.customer = customer
        self.start_label = start_label
        self.requests: dict = {}

    def add(self, req: AccessRequest) -> None:
        if req.key in self.requests:
            raise KeyError(f"duplicate request {req.key}")
        self.requests[req.key] = req

    def grant(self, key: str, day: int) -> None:
        r = self.requests[key]
        r.status, r.granted_day = "granted", day

    def ladder_position(self) -> str:
        """Highest rung for which every request on that rung and below is granted."""
        reached = "none"
        for rung in LADDER:
            on_rung = [r for r in self.requests.values() if r.rung == rung]
            if on_rung and all(r.status == "granted" for r in on_rung):
                reached = rung
            else:
                break
        return reached

    def waiting(self, today: int):
        open_ = [r for r in self.requests.values() if r.status in ("requested", "in review")]
        return sorted(open_, key=lambda r: -(r.days_open(today) or 0))

    def status_report(self, today: int) -> str:
        lines = [f"ACCESS STATUS  {self.customer}  day {today}",
                 f"{'request':<26}{'rung':<10}{'status':<15}{'days':>5}  owner / next action"]
        order = {k: i for i, k in enumerate(LADDER)}
        for r in sorted(self.requests.values(), key=lambda r: (order[r.rung], r.requested_day or 999)):
            d = r.days_open(today)
            ds = "-" if d is None else str(d)
            tail = r.owner + (f" / {r.next_action}" if r.next_action and r.status != "granted" else "")
            exp = r.next_expiry(today)
            if exp is not None:
                tail += f" / rotates day {exp}"
            lines.append(f"{r.key:<26}{r.rung:<10}{r.status:<15}{ds:>5}  {tail}")
        pos = self.ladder_position()
        rung_no = LADDER.index(pos) + 1 if pos in LADDER else 0
        w = self.waiting(today)
        lines.append(f"ladder: {pos} ({rung_no} of {len(LADDER)})   open requests: {len(w)}"
                     + (f"   longest wait: {w[0].key} ({w[0].days_open(today)} days, {w[0].owner})" if w else ""))
        blocked = sorted({b for r in w for b in r.blocks})
        if blocked:
            lines.append("blocked work: " + ", ".join(blocked))
        return "\n".join(lines)
