"""Listings 9.4 and 9.5: failure injection. A model asked to compute a loan-to-value ratio across three documents,
and the deterministic service that replaces it.

The documents are lab fixtures for a commercial-lending prospect (borrower Northgate Fabrication Ltd), amounts in
Canadian dollars. THE MODEL IS A DETERMINISTIC STAND-IN: no provider was called. It replays the four answer shapes a
model gives when handed this job whole (right; purchase price used as the value; prior charge left out; arithmetic
slip), with seeded frequencies that are parameters of the stand-in, not a measurement of any model.
"""
import random, re
from datetime import date

DOCS = {
    "appraisal.pdf": """APPRAISAL REPORT  Subject: 41 Keele Industrial Court  Client: lender
p3 l12  Market value as is, effective 14 August 2026: C$4,850,000
p3 l19  The subject was purchased in June 2019 for C$4,200,000.""",
    "term_sheet.pdf": """TERM SHEET  Borrower: Northgate Fabrication Ltd
p1 l08  Proposed senior term loan: C$2,900,000, second-ranking behind the existing charge
p1 l15  Policy: combined loan-to-value not to exceed 75% of appraised market value""",
    "charge_statement.pdf": """STATEMENT OF EXISTING CHARGES  Property: 41 Keele Industrial Court
p1 l06  First-ranking charge, balance at 30 September 2026: C$640,000
p1 l11  Original principal C$1,100,000 (registered 2019)""",
}
APPLICATION_DATE = date(2026, 10, 20)
POLICY_MAX = 0.75


# ---------------------------------------------------------------------------------- the stand-in model, whole job
SHAPES = [("right", 0.62), ("purchase price as value", 0.14),
          ("prior charge left out", 0.12), ("arithmetic slip", 0.12)]


def standin_model_ltv(rng):
    r = rng.random(); acc = 0
    for shape, p in SHAPES:
        acc += p
        if r < acc: break
    if shape == "right": v = 3_540_000 / 4_850_000
    elif shape == "purchase price as value": v = 3_540_000 / 4_200_000
    elif shape == "prior charge left out": v = 2_900_000 / 4_850_000
    else: v = 3_540_000 / 4_850_000 + rng.choice([-1, 1]) * rng.uniform(0.006, 0.03)
    return shape, round(v * 100, 1)


# ---------------------------------------------------------------------------------- the deterministic service
MONEY = r"C\$([\d,]+)"


class Refused(ValueError):
    pass


def cite(doc, pattern):
    """Return (amount, citation). A real deployment lets a constrained model propose the line; this check is the same:
    the cited line must contain the pattern and exactly one amount, or the service refuses."""
    for line in DOCS[doc].splitlines():
        if re.search(pattern, line, re.I):
            amts = re.findall(MONEY, line)
            if len(amts) != 1:
                raise Refused(f"{doc}: cited line has {len(amts)} amounts: {line.strip()}")
            return int(amts[0].replace(",", "")), f"{doc} {line.split()[0]} {line.split()[1]}"
    raise Refused(f"{doc}: no line matches {pattern!r}")


def ltv_service():
    value, c1 = cite("appraisal.pdf", r"market value as is")
    eff = re.search(r"effective (\d+) (\w+) (\d{4})", DOCS["appraisal.pdf"]).groups()
    eff_date = date(int(eff[2]), ["January", "February", "March", "April", "May", "June", "July", "August",
                                  "September", "October", "November", "December"].index(eff[1]) + 1, int(eff[0]))
    if (APPLICATION_DATE - eff_date).days > 365:
        raise Refused("appraisal older than twelve months")
    loan, c2 = cite("term_sheet.pdf", r"proposed senior term loan")
    prior, c3 = cite("charge_statement.pdf", r"first-ranking charge, balance")
    ltv = (loan + prior) / value
    lines = [f"value   {value:>12,}  {c1}  (effective {eff_date}, {(APPLICATION_DATE - eff_date).days} days old)",
             f"loan    {loan:>12,}  {c2}",
             f"prior   {prior:>12,}  {c3}",
             f"LTV = (loan + prior) / value = {loan + prior:,} / {value:,} = {ltv:.4f} -> {ltv:.1%}",
             f"policy max {POLICY_MAX:.0%}: {'within' if ltv <= POLICY_MAX else 'BREACH'}"]
    return ltv, lines


if __name__ == "__main__":
    rng = random.Random(2026)
    runs = [standin_model_ltv(rng) for _ in range(50)]
    print("STEP 1  the whole job to the model stand-in, 50 runs on the same three documents")
    for shape, _ in SHAPES:
        vals = sorted({v for s, v in runs if s == shape})
        n = sum(s == shape for s, _ in runs)
        print(f"  {shape:<26} {n:>3} runs  answers {', '.join(f'{v}%' for v in vals[:6])}{' ...' if len(vals) > 6 else ''}")
    wrong_side = sum((v / 100 > POLICY_MAX) != (3_540_000 / 4_850_000 > POLICY_MAX) for _, v in runs)
    off = sum(abs(v - 73.0) > 0.05 for _, v in runs)
    print(f"  answers not equal to 73.0%: {off} of 50; on the wrong side of the 75% policy line: {wrong_side} of 50")
    print("STEP 2  the deterministic service")
    ltv, lines = ltv_service()
    for l in lines: print("  " + l)
    print("STEP 3  the charge statement is restated: two amounts on the cited line")
    DOCS["charge_statement.pdf"] += "\np1 l14  First-ranking charge, balance restated: C$640,000 plus accrued C$12,400"
    DOCS["charge_statement.pdf"] = DOCS["charge_statement.pdf"].replace("First-ranking charge, balance at", "Superseded: balance at")
    try:
        ltv_service()
    except Refused as e:
        print(f"  REFUSED  {e}")
