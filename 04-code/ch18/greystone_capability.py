"""When the gateway lacks a capability: Greystone's catalog has no embedding model.

Deterministic stand-in: the catalog and the documentation page are fixtures; the 120 payer-criteria
passages and 80 referral queries are synthetic. Recall@5 is measured, by this script, on that stand-in.
"""
import _paths  # noqa: F401
import math, re
from collections import Counter
from fieldkit.gateway import capability_gap
from gateway_sim import h01

DOCS_PAGE = [{"capability": "chat", "name": "chat-standard"},
             {"capability": "embeddings", "name": "text-embed-legacy"}]          # page last edited 14 months ago
CATALOG = [{"capability": "chat", "name": "chat-standard", "status": "active"},
           {"capability": "chat", "name": "chat-mini", "status": "active"},
           {"capability": "embeddings", "name": "text-embed-legacy", "status": "removed"}]
REQUIRED = {"chat": ["referral summary draft", "prior-authorization letter draft"],
            "embeddings": ["payer-criteria retrieval"]}
for source, cat in (("documentation page", DOCS_PAGE), ("live catalog", CATALOG)):
    gaps = capability_gap(cat, REQUIRED)
    print(f"{source:<19}: " + "; ".join(f"{g['capability']} {'offered' if g['offered'] else 'MISSING'}" for g in gaps))

PAYERS = ["Front Range Health", "Mesa Plan", "Summit Care", "Plains Mutual", "Aspen Choice", "Granite Health",
          "Cedar Basic", "Pikes Network"]
PROCS = [("magnetic resonance imaging lumbar spine", ["MRI low back", "lumbar MRI"]),
         ("total knee arthroplasty", ["knee replacement", "TKA"]),
         ("sleep study polysomnography", ["sleep test", "overnight study"]),
         ("upper endoscopy", ["EGD", "scope of stomach"]),
         ("cardiac stress echocardiography", ["stress echo", "heart ultrasound with exercise"]),
         ("spinal cord stimulator trial", ["SCS trial", "stimulator for back pain"]),
         ("bariatric sleeve gastrectomy", ["weight loss surgery", "gastric sleeve"]),
         ("continuous glucose monitor", ["CGM", "glucose sensor"]),
         ("physical therapy extension", ["more PT visits", "PT renewal"]),
         ("computed tomography abdomen", ["CT belly", "abdominal CT"]),
         ("cataract extraction", ["cataract surgery", "lens replacement"]),
         ("home oxygen therapy", ["oxygen at home", "home O2"]),
         ("botulinum toxin for migraine", ["botox for headaches", "chemodenervation migraine"]),
         ("genetic panel hereditary cancer", ["BRCA testing", "cancer gene test"]),
         ("outpatient infusion biologic", ["infusion therapy", "biologic drip"])]
SYN = {s.lower(): p for p, ss in PROCS for s in ss[:1]}   # coordinators' table covers one synonym each
DOCS = []
for i, payer in enumerate(PAYERS):
    for j, (proc, _) in enumerate(PROCS):
        DOCS.append((i, j, f"{payer} prior authorization criteria for {proc}: documented "
                           f"conservative treatment, clinical notes within 90 days, ordering specialist"))
# Codes live in each policy's code table, which text extraction drops; kept here as structured data.
CODE_TABLE = {f"SC-{70100 + j * 7}": j for j in range(len(PROCS))}
tok = lambda s: re.findall(r"[a-z0-9-]+", s.lower())
N, avg = len(DOCS), sum(len(tok(d[2])) for d in DOCS) / len(DOCS)
df = Counter(w for d in DOCS for w in set(tok(d[2])))


def bm25(q, d, k1=1.2, b=0.75):
    tf, words = Counter(tok(d)), tok(d)
    return sum(math.log(1 + (N - df[w] + .5) / (df[w] + .5)) * tf[w] * (k1 + 1) /
               (tf[w] + k1 * (1 - b + b * len(words) / avg)) for w in set(tok(q)) if w in tf)


QUERIES = []
for q in range(80):
    i, j = int(h01("p", q) * 8), int(h01("r", q) * 15)
    proc, syns = PROCS[j]
    r = h01("wording", q)
    phrase = proc if r < 0.35 else syns[0] if r < 0.75 else syns[1]
    code = f" code SC-{70100 + j * 7}" if h01("code", q) < 0.5 else ""
    QUERIES.append((i, j, f"referral to {PAYERS[i]} for {phrase}{code}, patient failed six weeks of treatment"))


def search(query, use_codes, use_syn):
    qtext = query
    if use_syn:
        for s, p in SYN.items():
            if s in query.lower():
                qtext += " " + p
    m = re.search(r"SC-\d+", query)
    pool = DOCS
    if use_codes and m:
        exact = [d for d in DOCS if CODE_TABLE.get(m.group(0)) == d[1]]
        pool = exact or DOCS
    return sorted(pool, key=lambda d: -bm25(qtext, d[2]))[:5]


for name, codes, syn in (("lexical only", False, False), ("lexical + code lookup", True, False),
                         ("lexical + code lookup + synonym table", True, True)):
    hits = sum(any((d[0], d[1]) == (i, j) for d in search(text, codes, syn)) for i, j, text in QUERIES)
    print(f"{name:<38} recall@5 {hits}/80 = {hits / 80:.2f}")
