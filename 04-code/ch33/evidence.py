"""Listing 33.4: validation evidence for a model you do not own (deterministic stand-in for the provider model).

The stand-in reproduces Chapter 26's 76.7% field accuracy for p7 on the 201 gold-heldout documents. Each document
and field has a fixed latent state: reliably right, unstable (each run may differ) or reliably wrong. No model is
called; the 'runs' are draws from that state with fixed seeds, labeled as such in the chapter.
"""
import random
from world import M

FIELDS = ["policy_number", "claimant_name", "loss_date", "date_received", "loss_type", "loss_location",
          "injury_reported", "police_report_ref", "other_party", "intake_channel"]
ACC = dict(zip(FIELDS, [.90, .80, .78, .74, .79, .62, .84, .80, .62, .78]))
UNSTABLE = dict(zip(FIELDS, [.03, .08, .06, .07, .06, .20, .05, .05, .22, .04]))
COND = {"clean": {}, "fax noise": {"policy_number": .10, "police_report_ref": .14, "loss_date": .05,
                                     "date_received": .06},
        "rotated page": {"date_received": .31, "loss_date": .12, "policy_number": .08},
        "handwritten": {"claimant_name": .22, "loss_location": .18, "other_party": .16, "loss_date": .09}}
N, RUNS = 201, 20


def states(field, cond="clean"):
    rng = random.Random(f"{field}|states")
    drop = COND[cond].get(field, 0.0)
    out = []
    for d in range(N):
        u = rng.random()
        right, unst = ACC[field] - UNSTABLE[field] / 2 - drop, UNSTABLE[field] + drop / 2
        out.append("right" if u < right else "unstable" if u < right + unst else "wrong")
    return out


def runs(field, d, state, cond="clean"):
    rng = random.Random(f"{field}|{d}|{cond}|runs")
    if state == "right":
        return ["R"] * RUNS
    if state == "wrong":
        return ["W1"] * RUNS
    return [rng.choice(["R", "R", "W1", "W2"]) for _ in range(RUNS)]


def field_report(field, cond="clean"):
    st = states(field, cond)
    single = modal = varied = wrong_varied = wrong1 = 0
    agree = 0.0
    for d, s in enumerate(st):
        r = runs(field, d, s, cond)
        a, mode = M.repeat_agreement(r)
        agree += a
        single += r[0] == "R"; modal += mode == "R"
        v = a < 1.0
        varied += v
        if r[0] != "R":
            wrong1 += 1; wrong_varied += v
    return dict(single=single / N, modal=modal / N, agree=agree / N, varied=varied / N,
                wrong=wrong1, wrong_varied=wrong_varied)


if __name__ == "__main__":
    print(f"STABILITY: {N} gold-heldout documents, {RUNS} runs each at fixed settings (stand-in, pin extract-2026-04)")
    print(f"  {'field':<18} {'1 run':>6} {'modal':>6} {'agree':>6} {'varied':>7}  errors that varied")
    tot = dict(single=0, varied=0, wrong=0, wrong_varied=0)
    for f in FIELDS:
        r = field_report(f)
        for k in tot:
            tot[k] += r[k] * (N if k in ("single", "varied") else 1)
        print(f"  {f:<18} {r['single']:>6.1%} {r['modal']:>6.1%} {r['agree']:>6.3f} {r['varied']:>7.1%}  "
              f"{r['wrong_varied']} of {r['wrong']}")
    print(f"  {'all fields':<18} {tot['single'] / (N * 10):>6.1%} {'':>6} {'':>6} {tot['varied'] / (N * 10):>7.1%}  "
          f"{tot['wrong_varied']} of {tot['wrong']} ({tot['wrong_varied'] / tot['wrong']:.1%})")
    print()
    print("SENSITIVITY: single-run accuracy by condition (stand-in)")
    print(f"  {'field':<18} " + " ".join(f"{c:>13}" for c in COND))
    limits = []
    for f in FIELDS:
        acc = {c: field_report(f, c)["single"] for c in COND}
        print(f"  {f:<18} " + " ".join(f"{acc[c]:>13.1%}" for c in COND))
        for c in COND:
            if c != "clean" and acc["clean"] - acc[c] > 0.10:
                limits.append((f, c, acc["clean"] - acc[c]))
    print()
    print(f"LIMITS REGISTER: {len(limits)} field and condition pairs fall more than 10 points")
    for f, c, d in limits:
        print(f"  L-{FIELDS.index(f) + 1:02d} {f:<18} {c:<13} -{d * 100:.1f} points")
