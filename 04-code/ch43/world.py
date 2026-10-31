"""Chapter 43 lab world: the year after at Pennant and Caldwell, as a deterministic stand-in.

Start states are not invented here. Pennant's twenty hand-over items are Chapter 42's production-day-70 state
(readiness 0.80, recomputed from 04-code/ch42/ownership.py); Caldwell's are Chapter 41's day-183 state (0.90).
Rates: Northlight's loaded FDE rate is the book's $150 an hour (Chapter 2). Everything else (customer loaded rate,
fees, hours, practice schedules, events, renewal probabilities) is the lab's stand-in, labeled as such in the
output and recorded in the chapter ledger."""
import importlib.util
import pathlib
import sys
import _paths  # noqa: F401
from fieldkit.handover import Item, Step, Runbook, without, score
from fieldkit.service import Path, price_retainer

HERE = pathlib.Path(__file__).resolve().parent


def _load(name, folder, file):
    """Load another chapter's lab module without letting its world.py shadow this one."""
    d = str(HERE.parent / folder)
    saved = sys.modules.pop("world", None)
    sys.path.insert(0, d)
    try:
        spec = importlib.util.spec_from_file_location(name, f"{d}/{file}")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        sys.path.remove(d)
        sys.modules.pop("world", None)
        if saved is not None:
            sys.modules["world"] = saved
    return mod


W41 = _load("ch41world", "ch41", "world.py")
OWN42 = _load("ch42ownership", "ch42", "ownership.py")


def _pennant_day70():
    st = dict(W41.PENNANT)
    for _day, _what, ch, own in OWN42.EVENTS:
        for o in own:
            if o[0] == "leave":
                st = {i.id: (i.status, i.by) for i in without(OWN42.items(st), o[1])}
        st.update(ch)
    return st


def items(state):
    return [Item(i, d, t, state[i][0], state[i][1], g) for i, d, t, g in W41.ITEMS]


PENNANT0 = _pennant_day70()          # production day 70; unchanged to the decision on engagement day 261
CALDWELL0 = dict(W41.CALDWELL_AFTER)  # day 183; still 0.90 at Live Stable, engagement day 248
PN_START, CW_START = 289, 248         # Pennant's managed service starts day 290; Caldwell's retainer day 249

# ------------------------------------------------------------------ Pennant's four paths
CUSTOMER_RATE = 110.0    # Pennant's and Caldwell's loaded engineer rate, stand-in
NIGHT_ALLOWANCE = 2400.0  # Pennant on-call allowance for a 01:30 to 06:00 rota of four, per month, stand-in
RAMP = (60, 40, 20)       # extra customer hours while a night rota is built and trained
RET16, RET12 = price_retainer(16), price_retainer(12)

# items a managed service keeps the customer doing anyway, and the retention schedule Pennant signed
OPERATOR_ONLY = {"T1": 30, "C1": 365, "R1": 365}
RETENTION = dict(OPERATOR_ONLY, C1=180, R1=180, D1=90, R2=90, R3=90, D2=90, D3=180, M1=30, M2=30, M3=90, T3=90, T4=180, E1=180,
                 E2=180, E3=180, C2=180, M4=30, R4=180, T2=180)
PN_GROW = ((4, "alone", "T2", ("Kofi Mensah", "Nadia Brooks")), (6, "alone", "E3", ("Dana Whitaker", "Kofi Mensah")))

PENNANT_PATHS = {
    "hand-over": Path("hand-over: Pennant runs it alone", fee=0, vendor_hours=0, customer_hours=110,
                      customer_fixed=NIGHT_ALLOWANCE, ramp=RAMP, practice={"*": 90}, events=PN_GROW, renewal=0.85),
    "hybrid": Path("hybrid: Pennant runs it, 16-hour retainer", fee=RET16.fee, vendor_hours=12, customer_hours=100,
                   customer_fixed=NIGHT_ALLOWANCE, ramp=RAMP, practice={"*": 90}, events=PN_GROW, renewal=0.90),
    "managed-v0": Path("managed v0: Northlight runs it, as first quoted", fee=(18500, 24000), vendor_hours=96, customer_hours=14,
                       practice=OPERATOR_ONLY, events=((1, "lost", "M1"), (1, "lost", "M4")), vendor_only_steps=8,
                       renewal=0.95),
    "managed": Path("managed with retention: as signed", fee=(22000, 17000), vendor_hours=(96, 64),
                    customer_hours=(30, 48), practice=RETENTION,
                    events=((1, "lost", "M4"), (13, "alone", "M4", ("Andre Willis", "Nadia Brooks"))) + PN_GROW,
                    vendor_only_steps=0, renewal=0.92),
}

# ------------------------------------------------------------------ Caldwell: runs it alone, Northlight on retainer
_OC, _AK, _PN, _RC = "platform on-call rota", "Anne Kessler", "Priya Natarajan", "Ruth Calloway"
CALDWELL_PATHS = {
    "hybrid": Path("hybrid: Caldwell runs it, 12-hour retainer", fee=RET12.fee, vendor_hours=9, customer_hours=60,
                   practice={"*": 90},
                   events=((1, "alone", "M3", (_AK, _RC)), (3, "alone", "D2", (_OC, _PN)), (5, "alone", "T4", (_PN, _OC)),
                           (9, "leave", "Owen Pryce"), (10, "alone", "T3", (_RC,))), renewal=0.90),
    "managed": Path("managed (not chosen): Northlight runs it", fee=21000, vendor_hours=90, customer_hours=12,
                    practice=OPERATOR_ONLY, events=((1, "lost", "M1"), (1, "lost", "M4")), vendor_only_steps=0,
                    renewal=0.95),
}

# ------------------------------------------------------------------ the managed-service runbooks (failure injection)
OWNERS = {
    "console.pennant.example": "customer", "gs://pennant-matching-prod": "customer",
    "github.com/pennant-it/matching-evals": "customer", "vault:pennant/provider": "customer",
    "tms-mft.pennant.example": "customer", "modectl.pennant.example": "customer",
    "ops.northlight.example": "Northlight", "nl-bastion-02": "Northlight",
    "github.com/northlight-ai/pennant-evals": "Northlight", "s3://nl-evidence/pennant": "Northlight",
    "vault:northlight/pennant": "Northlight", "status.northlight.example": "Northlight",
}
_NL, _PC = "Northlight on-call (night)", "Pennant on-call (day)"
RB_V0 = (
    Runbook("MS-RB-01", "TMS feed late or missing", "P-01", "data", "off", "Rosa Delgado", (
        Step("open ops.northlight.example and read the feed status for the 02:00 file", _NL, "status page shows file age"),
        Step("ssh to nl-bastion-02 and tail the loader log", _NL, "last line names the file"),
        Step("set mode off at modectl.pennant.example", _NL, "mode reads off"),
        Step("ask Kofi Mensah's team to resend the CSV to tms-mft.pennant.example", _NL, "file lands with today's date"),
        Step("reconcile counts, then return via shadow at modectl.pennant.example", _NL, "counts match the TMS"),
    ), exit_via="shadow"),
    Runbook("MS-RB-02", "matched rate below the line", "P-02", "quality", "shadow", "Dana Whitaker", (
        Step("set mode shadow at modectl.pennant.example", _NL, "mode reads shadow"),
        Step("run the evaluation suite from github.com/northlight-ai/pennant-evals", _NL, "suite report written"),
        Step("compare against the gold set in s3://nl-evidence/pennant", _NL, "comparison has 200 rows"),
        Step("Dana Whitaker re-scores 50 flagged documents", "Dana Whitaker", "50 scored"),
    )),
    Runbook("MS-RB-03", "provider errors or key expiry", "P-03", "availability", "fail-closed", "Kofi Mensah", (
        Step("confirm fail-closed at modectl.pennant.example", _NL, "no documents released"),
        Step("rotate the provider key from vault:northlight/pennant", _NL, "test call returns 200"),
        Step("post the incident note on status.northlight.example", _NL, "note visible to Pennant"),
    )),
    Runbook("MS-RB-04", "EU model change", "P-04", "quality", "shadow", "Joanne Pruitt", (
        Step("pin the candidate in shadow at modectl.pennant.example", _NL, "pin recorded"),
        Step("run the comparison from github.com/northlight-ai/pennant-evals", _NL, "comparison written"),
        Step("store the evidence pack in s3://nl-evidence/pennant/eu", _NL, "pack hash recorded"),
        Step("Joanne Pruitt approves or rejects under change control", "Joanne Pruitt", "decision in the register"),
    )),
)
_SUB = {"ops.northlight.example": "console.pennant.example", "nl-bastion-02": "console.pennant.example",
        "github.com/northlight-ai/pennant-evals": "github.com/pennant-it/matching-evals",
        "s3://nl-evidence/pennant/eu": "gs://pennant-matching-prod/evidence/eu",
        "s3://nl-evidence/pennant": "gs://pennant-matching-prod/evidence", "vault:northlight/pennant": "vault:pennant/provider",
        "status.northlight.example": "console.pennant.example/status"}


def _v1(rb):
    def fix(t):
        for a, b in _SUB.items():
            t = t.replace(a, b)
        return t.replace("ssh to console.pennant.example and tail", "open console.pennant.example and read")
    return Runbook(rb.id, rb.title, rb.trigger, rb.failure_class, rb.mode, rb.owner,
                   tuple(Step(fix(s.action), s.by_role.replace(_NL, f"{_NL}; {_PC}"), fix(s.verify)) for s in rb.steps),
                   rb.exit_via)


RB_V1 = tuple(_v1(r) for r in RB_V0)
PN_PEOPLE = {"Grant Holloway", "Rosa Delgado", "Dana Whitaker", "Tasha Greene", "Kofi Mensah", "Joanne Pruitt",
             "Andre Willis", "Nadia Brooks", "Marisol Vega", "Annelies de Vries"}
PN_ALERTS = [W41.Alert(f"P-0{i}", f"monitor {i}", "pennant-oncall@pennant.example") for i in range(1, 5)]
DRILL_MINUTES = (6, 9, 2, 25, 18)    # MS-RB-01 step times at Pennant, stand-in; feed due 02:00, deadline 03:30
DRILL_WORKAROUND = {"ops.northlight.example": ("Pennant cloud console, loader job history", 31)}
