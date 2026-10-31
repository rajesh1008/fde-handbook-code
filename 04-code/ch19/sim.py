"""Deterministic stand-ins for Chapter 19: Caldwell's claims-core (2009), its sample of 200 documents, and
Pennant's nightly TMS export and carrier EDI. Nothing here is customer data and nothing calls a model.
The extraction step is a deterministic stand-in: fields come from the sample's gold values, and a cause-of-loss
code is missing exactly where the source document does not state one."""
import datetime as dt
import random

FIRST = ["Emily", "Robert", "Maria", "James", "Aisha", "Daniel", "Grace", "Omar", "Linda", "Kevin", "Sofia", "Paul"]
LAST = ["Carter", "Hayes", "Lopez", "Nguyen", "Brooks", "Patel", "Kim", "Foster", "Rivera", "Coleman", "Ward", "Price"]
TYPES = ["fire", "theft", "auto_collision", "wind"]
CAUSE = {"water": ["WB01 burst pipe", "WS02 sewer backup", "WF03 surface flood"]}


def caldwell_sample(seed=19):
    """200 documents: 152 first notices of loss, 48 supporting documents; channels 88 mail, 71 scan, 41 fax."""
    rng = random.Random(seed)
    ch = ["mail"] * 88 + ["scan"] * 71 + ["fax"] * 41
    kind = ["fnol"] * 152 + ["support"] * 48
    rng.shuffle(ch); rng.shuffle(kind)
    docs, fn = [], 0
    base = dt.date(2026, 7, 6)
    fnol_idx = [i for i, k in enumerate(kind) if k == "fnol"]
    water = set(rng.sample(fnol_idx, 31))
    no_cause = set(sorted(water)[::3][:11])
    rest = [i for i in fnol_idx if i not in water]
    old_loss, long_name = rest[7], rest[19]
    timeouts = {rest[30], rest[55], rest[90]}
    for i in range(200):
        rep = base + dt.timedelta(days=i % 40)
        d = {"doc": f"CS200-{i + 1:03d}", "channel": ch[i], "kind": kind[i]}
        if kind[i] == "fnol":
            fn += 1
            name = f"{FIRST[i % 12]} {LAST[(i * 7) % 12]}"
            if i == long_name:
                name = "Northgate Fabrication Ltd Employee Benefit Trust"
            loss = rep - dt.timedelta(days=400 if i == old_loss else rng.randint(0, 20))
            lt = "water" if i in water else rng.choice(TYPES)
            d.update(policy_no=f"CM-{4100000 + i * 37}", claimant=name, loss_type=lt,
                     cause_code=None if (lt != "water" or i in no_cause) else rng.choice(CAUSE["water"])[:4],
                     loss_date=loss.isoformat(), report_date=rep.isoformat(), zip=f"06{rng.randint(100, 999)}",
                     timeout=i in timeouts)
        else:
            d.update(claim_ref=f"CC-{20240000 + i * 11}", archived=i in (rest[3], rest[4]) or False)
        docs.append(d)
    sup = [d for d in docs if d["kind"] == "support"]
    for d in sup[5], sup[29]:
        d["archived"] = True
    return docs


# ---------------------------------------------------------------- claims-core
def r_v031(r): return r["policy_no"].startswith("CM-")
def r_v118(r): return not (r["loss_type"] == "water" and not r.get("cause_code"))
def r_v127(r):
    return (dt.date.fromisoformat(r["report_date"]) - dt.date.fromisoformat(r["loss_date"])).days <= 365

RULES = {"V-031": ("policy exists and is in force on the loss date", r_v031),
         "V-118": ("a water loss needs a cause-of-loss code (added 2024)", r_v118),
         "V-127": ("loss date at most 365 days before report date (added day 69)", r_v127)}
ENV_RULES = {"uat": ["V-031"], "preprod": ["V-031", "V-118", "V-127"]}

FNOL1 = ["Policy No", "Claimant", "Loss Date", "Loss Type", "Agent Ref"]
FNOL2 = ["Report Date", "Cause of Loss", "Loss ZIP", "Description"]


class ClaimsCore:
    """A 2009 claims system reached only through its screens. FNOL-1 creates a claim shell and commits it;
    FNOL-2 runs the rule table and completes the claim. The claimant field silently truncates at 30 characters.
    'Agent Ref' is a free-text field Caldwell agreed to lend us for the intake key."""

    def __init__(self, env, lose_response=(), patched=False):
        self.env, self.rules = env, ENV_RULES[env]
        self.lose = set(lose_response); self.lost_once = set()
        self.claims, self.n, self.patched = {}, 0, patched

    # screen surface
    def labels(self, name):
        if name == "FNOL-1":
            return (FNOL1[:2] + ["Reported By"] + FNOL1[2:]) if self.patched else FNOL1
        return FNOL2

    def submit(self, name, values, key):
        if name == "FNOL-1":
            self.n += 1
            cid = f"CC-{20260000 + self.n}"
            self.claims[cid] = {"status": "SHELL", "Agent Ref": key, **values,
                                "Claimant": str(values.get("Claimant", ""))[:30]}
            return True, cid, None
        cid = values.pop("_cid")
        c = self.claims[cid]; c.update(values)
        rec = {"policy_no": c["Policy No"], "loss_type": c["Loss Type"], "cause_code": c.get("Cause of Loss"),
               "loss_date": c["Loss Date"], "report_date": c["Report Date"]}
        failed = [r for r in self.rules if not RULES[r][1](rec)]
        if failed:
            return False, cid, ",".join(failed)
        c["status"] = "OPEN"
        if key in self.lose and key not in self.lost_once:
            self.lost_once.add(key)
            raise TimeoutError("session expired before the confirmation page")
        return True, cid, None

    def read(self, name, cid):
        return self.claims[cid]

    def void(self, cid):
        self.claims[cid]["status"] = "VOID"; return True

    def extract(self):
        """The next-morning warehouse extract: what the system of record says, not what we logged."""
        return [dict(cid=k, **v) for k, v in self.claims.items()]


FIELD = {"policy_no": "Policy No", "claimant": "Claimant", "loss_date": "Loss Date", "loss_type": "Loss Type",
         "report_date": "Report Date", "cause_code": "Cause of Loss", "zip": "Loss ZIP"}


def as_record(c):
    return {f: c.get(lbl) for f, lbl in FIELD.items()}


# ---------------------------------------------------------------- Pennant
HEADER = ["shipment_id", "leg_no", "origin", "dest", "carrier_scac", "status", "status_ts", "export_ts"]
SCAC = ["BRFR", "HLSH", "MDXP", "GLTR", "CRWN", "NWAY", "RVRL", "TSPN", "KSTL", "ATLC", "PRMT"]
STATUSES = ["picked_up", "departed", "en_route", "arrived", "delivered", "delayed", "estimated"]


def nightly_csv(night, rows=None, header=None, seed=0):
    rng = random.Random(1000 + night + seed)
    wd = dt.date(2026, 9, 1) + dt.timedelta(days=night - 1)
    n = rows if rows is not None else (rng.randint(36600, 39400) if wd.weekday() < 5 else rng.randint(8200, 9800))
    h = header or HEADER
    out = [",".join(h)]
    for k in range(n):
        out.append(f"PL{night:02d}{k:06d},{1 + k % 3},MEM,{['ATL','DFW','CHI','RTM','HAM'][k % 5]},"
                   f"{SCAC[k % 11]},{STATUSES[k % 7]},{wd.isoformat()}T{k % 24:02d}:00,{wd.isoformat()}T02:00")
    return "\n".join(out).encode(), wd


def x12_214(ctrl, ship, leg, code, date, time, bad_count=False):
    st = f"{ctrl:04d}"
    body = [f"ST*214*{st}", f"B10*{ship}*{ship}*{SCAC[ctrl % 11]}", f"L11*{leg}*LG",
            f"AT7*{code}*NS***{date}*{time}", "MS1*MEMPHIS*TN*US"]
    se = len(body) + 1 + (1 if bad_count else 0)
    return "~".join(body + [f"SE*{se}*{st}"])


def edi_day(seed=214):
    """One day of carrier status messages: 312 sets; 4 with a wrong SE count, 3 with an unknown status code.
    Returns the interchange text and the truth (what the TMS shows at the next 02:00 export)."""
    rng = random.Random(seed)
    sets, truth = [], {}
    codes = [c for c in ["X3", "AF", "X6", "X4", "D1", "SD"]]
    bad_se = set(rng.sample(range(312), 4))
    unk = set(rng.sample([i for i in range(312) if i not in bad_se], 3))
    for i in range(312):
        ship, leg = f"PL30{rng.randint(0, 36000):06d}", str(1 + i % 3)
        code = "ZZ" if i in unk else rng.choice(codes)
        sets.append(x12_214(i + 1, ship, leg, code, "20260930", f"{6 + i % 14:02d}{(i * 7) % 60:02d}", i in bad_se))
        truth[(ship, leg)] = code
    isa = "ISA*00*          *00*          *ZZ*PENNANTVAN     *ZZ*PENNANT        *260930*2359*U*00401*000000930*0*P*>"
    return "~".join([isa] + sets + ["IEA*1*000000930"]), truth
