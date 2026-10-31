"""Deterministic stand-in for Caldwell Mutual's claims policy library and Anne Kessler's question set.
Nothing here is Caldwell data. The library, its ACLs, its four-version water-loss section and the questions are
generated from a fixed seed so every number in Chapter 23 can be re-run. The embedding is a stand-in for the
gateway's embedding deployment: it knows some of the adjusters' phrasings and none of Caldwell's identifiers."""
import random, re
import _paths  # noqa: F401
from fieldkit.retrieval import Index, Principal, Question, tokens

SEED = 23
# manual wording | how adjusters say it
DETAILS = """water heater|hot water tank;sump pump|basement pump;ice dam|ice buildup on the roof;supply line|braided hose;
roof decking|roof boards;drywall|sheetrock;subfloor|floor under the carpet;mold remediation|mold cleanup;
moisture reading|wet meter number;drying log|dehumidifier record;mitigation vendor|cleanup company;
contents inventory|list of belongings;additional living expense|hotel money;actual cash value|depreciated payout;
replacement cost holdback|recoverable depreciation;proof of loss|sworn statement;examination under oath|sworn interview;
reservation of rights|ror letter;coverage position letter|denial letter;recorded statement|phone interview;
police report|incident report number;total loss threshold|totaled car;salvage title|branded title;
rental reimbursement|rental car coverage;diminished value|lost resale value;glass repair|windshield chip;
deductible waiver|no deductible;hail damage|hail dents;wind speed report|weather data;catastrophe code|storm number;
tarp invoice|emergency roof cover;contractor estimate|repair quote;desk adjuster|inside adjuster;
field inspection|site visit;independent appraiser|outside appraiser;appraisal clause|umpire process;
subrogation notice|recovery letter;tortfeasor carrier|other driver insurer;arbitration forum|intercompany arbitration;
lienholder|bank on the title;mortgagee clause|mortgage company on the check;payee names|who goes on the check;
reserve change|bump the reserve;supervisor approval|manager sign off;authority limit|how much I can pay;
large loss report|big claim writeup;litigation hold|preservation notice;claimant attorney|plaintiff lawyer;
medical authorization|hipaa release;bodily injury|injury claim;medical payments|med pay;prior loss history|previous claims;
index bureau report|claims database hit;late notice|reported late;vacancy clause|empty house;frozen pipes|pipes froze;
gradual leak|slow drip;continuous seepage|leaking for months;wear and tear|old roof;cause code|why it happened code;
date of loss|when it happened;policy period|when the policy was active;endorsement schedule|list of add ons;
named storm deductible|hurricane deductible;ordinance or law|code upgrade;debris removal|haul away;
tree removal|fallen tree;fence damage|broken fence;detached structure|garage or shed;personal property limit|contents cap;
scheduled jewelry|ring rider;theft affidavit|stolen items form;forced entry|break in signs;
vehicle recovery|car found;catalytic converter|cat converter;towing invoice|tow bill;storage fees|yard fees;
title transfer|sign over the title;gap coverage|loan gap;rental extension|more rental days;first notice of loss|first call;
acknowledgment letter|we got your claim letter;status letter|update letter;payment hold|stop the check;
duplicate payment|paid twice;check reissue|new check;electronic payment|direct deposit;
regulatory deadline|days to respond;claim closure|close the file;reopened claim|reopen the file;file note|diary entry;
diary date|follow up date"""
TOPICS = """water loss|water damage;wind and hail|storm damage;theft|stolen stuff;collision|car accident;glass|windshield;
total loss|totaled vehicle;subrogation|recovery;appraisal|appraisal dispute;reserves|reserving;payments|paying out;
correspondence|letters to the insured;regulatory timing|state deadlines;catastrophe handling|cat event;
contents|personal property;living expense|displacement;liability|third party;medical|injury handling;
coverage verification|checking coverage;dwelling|house damage;mold|fungus;fire and smoke|fire damage;roof|shingles;
vehicle theft|stolen car;rental|loaner;lien and mortgagee|lienholders;closing and reopening|file closure;
complaints|unhappy insureds;vacancy|vacant homes;siu referral|fraud red flags;litigation management|lawsuits;
employee claims|claims by staff;large loss authority|big loss approvals"""
pairs = lambda s: [tuple(x.strip().split("|")) for x in s.replace("\n", "").split(";")]
DET, TOP = pairs(DETAILS), pairs(TOPICS)
RESTRICTED = {"siu referral": "claims-siu", "litigation management": "claims-litigation",
              "employee claims": "claims-employee", "large loss authority": "claims-mgmt"}
VERBS = ["confirms", "documents", "requests", "reviews", "verifies", "attaches", "notes", "escalates"]
STOP = set("the a an of in on to and or for is be by with within before after when what how do we does i can my it".split())


def _known_slang():
    """The stand-in embedding model 'knows' about 55% of adjuster phrasings (general English) and no identifiers."""
    r = random.Random(SEED + 1); m = {}
    for man, sl in DET + TOP:
        if r.random() < 0.80:
            for w in tokens(sl):
                if w not in STOP:
                    m.setdefault(w, tokens(man))
    return m


KNOWN = _known_slang()


def embed(text):
    """Stand-in for the gateway embedding deployment: drops identifiers and stop words, folds plurals,
    maps the phrasings it knows onto the manual's words."""
    v = {}
    for w in tokens(text):
        if w in STOP or any(ch.isdigit() for ch in w):
            continue
        for t in KNOWN.get(w, [w]):
            t = t[:-1] if t.endswith("s") and len(t) > 3 else t
            v[t] = v.get(t, 0.0) + 1.0
    return v


def library():
    """Returns (records, source_acl, versions) for the claims policy library as Caldwell's document system holds it:
    every file carries its ACL; old versions sit beside new ones with nothing saying which applies."""
    r = random.Random(SEED); recs = []; acl = {}; versions = {}
    for ti, (topic, _) in enumerate(TOP):
        group = RESTRICTED.get(topic, "claims-all")
        code = "".join(w[0] for w in topic.split()).upper()[:3] + f"{ti:02d}"
        for d in range(19):
            doc = f"CM-{code}-{d + 1:02d}"; acl[doc] = [group]
            nver = 1 if r.random() > 0.12 else r.choice([2, 3])
            n = r.randint(7, 11); passages = []
            for k in range(n):
                ds = r.sample(DET, 3); form = r.random() < 0.08
                fid = f"CF {r.randint(10, 99):02d} {r.randint(10, 99):02d}" if form else ""
                days = r.choice([2, 3, 5, 10, 15, 30])
                txt = (f"{topic.capitalize()}. {'Form ' + fid + ': ' if fid else ''}The adjuster {r.choice(VERBS)} the "
                       f"{ds[0][0]} and the {ds[1][0]}, then records the {ds[2][0]} in the file note within {days} days.")
                passages.append(dict(k=k, ds=ds, fid=fid, days=days, txt=txt))
            for v in range(nver):
                eff = 20190301 + 10000 * (2 * v + r.randint(0, 1))
                state = "current"  # the source has no lifecycle field at all
                for p in passages:
                    txt = p["txt"] if v == nver - 1 else p["txt"].replace(f"within {p['days']} days", f"within {p['days'] + 5} days")
                    recs.append(dict(pid=f"{doc}-v{v + 1}-p{p['k']:02d}", doc_id=f"{doc}-v{v + 1}", version=str(v + 1),
                                     section=f"{topic} {doc}", text=txt, acl=[group], effective_from=eff, state=state,
                                     topic=topic, details=p["ds"], fid=p["fid"], latest=v == nver - 1))
                acl[f"{doc}-v{v + 1}"] = [group]
            versions[doc] = nver
            del acl[doc]
    recs += water_loss_versions(); acl.update({f"CM-WL-07-v{i}": ["claims-all"] for i in range(1, 5)})
    return recs, acl, versions


WL = [  # the sidebar: one section, four files in the same folder
 ("1", 20190301, "Water loss. Cause code for supply line and water heater losses: the desk adjuster selects a cause code "
                 "when the cause is clear; where the cause is unclear the cause code is optional."),
 ("2", 20220601, "Water loss. Cause code for supply line losses: the cause code is optional at first notice of loss. "
                 "The desk adjuster may leave the cause code blank until the field inspection, and the field inspection "
                 "sets the cause code when the desk adjuster left it blank."),
 ("3", 20240901, "Water loss. A cause code is required on every water loss, supply line losses included, before any "
                 "reserve change or payment (validation rule V-118); the desk adjuster may not leave the cause code blank "
                 "pending field inspection. Gradual leak and continuous seepage take their own cause code."),
 ("4", 20260701, "Water loss. Draft for review: a cause code is required at first notice of loss on every water loss, "
                 "and the desk adjuster may not save the claim with the cause code blank."),
]


def water_loss_versions():
    return [dict(pid=f"CM-WL-07-v{v}-p00", doc_id=f"CM-WL-07-v{v}", version=v, section="water loss CM-WL-07",
                 text=t, acl=["claims-all"], effective_from=e, state="current", topic="water loss",
                 details=(), fid="", latest=v == "3") for v, e, t in WL]


def lifecycle_register(versions):
    """What Joan Mercer (claims procedures manager) signed on day 106: per document, which version applies,
    which are superseded and from when, which are drafts. Effective dates come from the files' own headers."""
    reg = []
    for doc, n in sorted(versions.items()):
        for v in range(1, n):
            reg.append((f"{doc}-v{v}", "superseded", f"{doc}-v{v + 1}"))
    reg += [("CM-WL-07-v1", "superseded", "CM-WL-07-v2"), ("CM-WL-07-v2", "superseded", "CM-WL-07-v3"),
            ("CM-WL-07-v4", "draft", None)]
    return reg


def apply_register(ix, reg):
    eff = {p.doc_id: p.effective_from for p in ix.passages.values()}
    n = 0
    for doc, state, succ in reg:
        n += ix.set_state(doc, state, superseded_by=succ, on=eff.get(succ) if succ else None, by="Joan Mercer")
    return n


def build(day=88):
    recs, acl, versions = library()
    ix = Index(embed=embed); ix.ingest(recs, day=day)
    return ix, recs, acl, versions


PEOPLE = {"tom": Principal("tom.whitfield", frozenset({"claims-all"})),
          "siu": Principal("siu.investigator", frozenset({"claims-all", "claims-siu"})),
          "anne": Principal("anne.kessler", frozenset({"claims-all", "claims-siu", "claims-litigation",
                                                       "claims-employee", "claims-mgmt"}))}

NO_ANSWER = ["How do we handle an NFIP flood claim for a basement", "What is the pet injury sublimit on a homeowners policy",
             "Who approves a cyber extortion payment", "Can we pay crypto wallet theft under contents",
             "How is earthquake sprinkler leakage adjusted in Vermont", "What is the drone inspection vendor rate",
             "Does the umbrella policy cover boat liability", "How do we adjust a commercial crop hail loss",
             "What is the title insurance claim process", "How is a pet health claim reopened",
             "Who signs off identity theft restoration services", "How do we handle a farm equipment breakdown",
             "What is the travel insurance cancellation rule", "Can a tenant claim against a landlord bond",
             "How is a life insurance beneficiary verified"]


def questions(recs, slang=0.37, synthetic=False, seed=SEED + 2):
    """Anne Kessler's set: 150 questions written by three adjuster teams, gold passages marked by two adjusters,
    disagreements settled by Anne. Categories as Anne's teams labeled them. synthetic=True builds the vendor-style
    set instead: questions generated from the passages' own words."""
    r = random.Random(seed)
    cur = [p for p in recs if p["latest"] and p["details"]]
    multi = [p for p in cur if p["version"] != "1"]
    forms = [p for p in cur if p["fid"]]
    say = lambda pair: pair[0] if synthetic or r.random() > slang else pair[1]
    topic_say = {m: s for m, s in TOP}
    qs = []

    def one(p):
        t = (p["topic"], topic_say[p["topic"]])
        return f"{say(t)} {say(p['details'][0])} {say(p['details'][1])}"

    asker = lambda p: "siu" if p["acl"] == ["claims-siu"] else ("anne" if p["acl"] != ["claims-all"] else "tom")
    for i, p in enumerate(r.sample(cur, 62)):
        qs.append(Question(f"A{len(qs) + 1:03d}", "What does the manual say about " + one(p), "procedure lookup",
                           (p["pid"],), asked_by=asker(p)))
    for p in r.sample(forms, 28):
        qs.append(Question(f"A{len(qs) + 1:03d}", f"Form {p['fid']} {say(p['details'][0])}", "form or code",
                           (p["pid"],), asked_by=asker(p)))
    for p in r.sample(multi, 24):
        qs.append(Question(f"A{len(qs) + 1:03d}", "Current rule: " + one(p), "version-sensitive",
                           (p["pid"],), asked_by=asker(p)))
    open_ = [p for p in cur if p["acl"] == ["claims-all"]]
    for _ in range(21):
        a, b = r.sample(open_, 2)
        while a["topic"] == b["topic"]:
            a, b = r.sample(open_, 2)
        qs.append(Question(f"A{len(qs) + 1:03d}", one(a) + " and " + one(b), "cross-document",
                           (a["pid"], b["pid"]), asked_by="tom"))
    for t in NO_ANSWER:
        qs.append(Question(f"A{len(qs) + 1:03d}", t, "not in the documents", (), asked_by="tom"))
    return qs


def who_for(q):
    return PEOPLE[q.asked_by]
