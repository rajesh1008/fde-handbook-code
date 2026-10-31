"""Chapter 30 world: Caldwell's document-type step (C06) as a deterministic stand-in.

Nothing here is Caldwell data. Documents are bags of tokens generated from fixed seeds so every number in the
chapter re-runs exactly. Classes are the four signed types and "none" (Chapter 8, criterion C-01):
T1 Caldwell first-notice form, T2 agency first-notice form, T3 first-notice letter or email, T4 repair estimate,
none (medical, police, photographs and other correspondence, attorney letters).
"""
import _paths  # noqa: F401
import numpy as np
from dataclasses import dataclass, field

CLASSES = ["T1", "T2", "T3", "T4", "none"]
KINDS = {  # kind -> true class
    "T1": "T1", "T2": "T2", "T2p": "T2", "T3": "T3", "T4": "T4", "T4s": "T4",
    "medical": "none", "police": "none", "corr": "none", "attorney": "none",
}
# T2p: agency form filed on Caldwell's portal template (looks like T1; the footer says agency).
# T4s: repair-estimate supplement on an existing claim (T4 under the day-28 scope; Joan Mercer's day-146 ruling
#      makes it "none", other correspondence). corr: correspondence about an existing claim (looks like T3).
CONDITIONS = {"clean": (0.05, 0.02), "medium": (0.35, 0.22), "hard": (0.65, 0.50)}  # (drop, junk) rates


def _vocab(prefix, n):
    return [f"{prefix}{i}" for i in range(n)]


V = {
    "common": _vocab("w", 220), "form": _vocab("form", 40), "letter": _vocab("let", 40),
    "loss": _vocab("loss", 30), "claimref": _vocab("ref", 12), "t1": _vocab("cmfn", 14),
    "agency": _vocab("agy", 30), "est": _vocab("est", 40), "supp": _vocab("supp", 8), "med": _vocab("med", 40),
    "police": _vocab("pol", 40), "photo": _vocab("pho", 25), "atty": _vocab("atty", 30), "junk": _vocab("junk", 400),
}
RECIPE = {  # kind -> list of (vocabulary, count)
    "T1": [("common", 30), ("form", 22), ("loss", 8), ("t1", 6)],
    "T2": [("common", 30), ("form", 20), ("loss", 8), ("agency", 7)],
    "T2p": [("common", 30), ("form", 22), ("loss", 8), ("t1", 4), ("agency", 2)],
    "T3": [("common", 40), ("letter", 18), ("loss", 12)],
    "T4": [("common", 25), ("est", 25), ("loss", 3)],
    "T4s": [("common", 25), ("est", 22), ("loss", 2), ("supp", 3), ("claimref", 2)],
    "medical": [("common", 25), ("med", 25)],
    "police": [("common", 25), ("police", 25), ("loss", 5)],
    "corr": [("common", 40), ("letter", 18), ("loss", 6), ("claimref", 2), ("photo", 3)],
    "attorney": [("common", 40), ("letter", 18), ("loss", 10), ("atty", 8)],
}


@dataclass
class Doc:
    id: str
    kind: str
    condition: str
    tokens: list = field(repr=False)
    label: str = ""          # the label this set carries (clerk or adjuster)

    @property
    def truth(self):
        return KINDS[self.kind]


def make_doc(rng, did, kind, condition):
    toks = []
    for voc, n in RECIPE[kind]:
        toks += list(rng.choice(V[voc], size=n))
    drop, junk = CONDITIONS[condition]
    keep = [t for t in toks if rng.random() >= drop]
    nj = int(round(junk * len(toks)))
    keep += list(rng.choice(V["junk"], size=nj))
    if kind == "attorney":  # letterhead firm code, drawn from the id hash so no other document changes
        keep.append(f"firm{int(h('firm:' + did) * 200)}")
    return Doc(did, kind, condition, keep)


# The legal mail coordinator's registry of firms that write to Caldwell (170 of the 200 firm codes in the world).
REGISTRY = frozenset(f"firm{i}" for i in range(170))


def make_set(name, seed, kind_counts, cond_p, clerk_noise=0.0):
    rng = np.random.default_rng(seed)
    docs, i = [], 0
    conds = list(CONDITIONS)
    for kind, n in kind_counts.items():
        for _ in range(n):
            c = conds[rng.choice(3, p=cond_p)]
            d = make_doc(rng, f"{name}-{i:05d}", kind, c)
            d.label = d.truth
            if clerk_noise and rng.random() < clerk_noise:
                d.label = CLASSES[(CLASSES.index(d.truth) + 1 + rng.integers(4)) % 5]
            docs.append(d); i += 1
    order = rng.permutation(len(docs))
    return [docs[j] for j in order]


# history-6000: documents attached to claims by intake clerks, with the clerk's type code (labels about 3% noisy).
# Attorney letters never pass through intake clerks (they go to legal), so the kind is absent from this set.
HISTORY_COUNTS = {"T1": 2050, "T2": 760, "T2p": 220, "T3": 1050, "T4": 560, "T4s": 90, "medical": 380,
                  "police": 400, "corr": 490}
# anne-900: gold-set-300 plus cal-600, drawn from intake paths P01 to P07 to Anne Kessler's strata and labeled by
# her adjusters. Five misfiled attorney letters arrived through the main paths and are in it.
ANNE_COUNTS = {"T1": 305, "T2": 113, "T2p": 44, "T3": 162, "T4": 92, "T4s": 7, "medical": 52, "police": 54,
               "corr": 66, "attorney": 5}


def history():
    return make_set("hist", 3001, HISTORY_COUNTS, [0.80, 0.17, 0.03], clerk_noise=0.012)


def split(docs, test_share=0.2):
    n = int(len(docs) * (1 - test_share))
    return docs[:n], docs[n:]


def anne():
    return make_set("anne", 3013, ANNE_COUNTS, [0.48, 0.34, 0.18])


def legal60():
    """The legal mail coordinator's misfile register: 60 attorney letters that arrived through main intake paths."""
    return make_set("legal", 3003, {"attorney": 60}, [0.55, 0.40, 0.05])


def supplements(n=80, seed=3004):
    """Repair-estimate supplements, labeled under Joan Mercer's day-146 ruling (other correspondence: none)."""
    s = make_set("supp", seed, {"T4s": n}, [0.6, 0.35, 0.05])
    for d in s:
        d.label = "none"
    return s


def h(s):
    import hashlib
    return int(hashlib.sha256(s.encode()).hexdigest()[:12], 16) / 16 ** 12
