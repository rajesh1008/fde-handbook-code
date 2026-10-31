"""Listing 4.7: three timelines for the same five gates. The deal sheet and the Chapter 2 field estimate
are carried forward [CHECK ch02]; the re-baselined plan is what Daniel Reyes accepted on day 12."""
GATES = ("Architecture Review", "Build Complete", "Shadow Exit", "Model-Risk Approval", "Live Stable")
DEAL_SHEET = (15, 120, 124, 129, 135)
FIELD_ESTIMATE = (64, 209, 230, 251, 268)
# Re-baselined day 12: ranges, each conditional on a dependency with a named owner.
REBASELINED = [
    ("Architecture Review", 40, 60, "claims-core read-only access (requested day 5)", "Daniel Reyes"),
    ("Build Complete", 85, 100, "gold set scored by adjusters", "Anne Kessler"),
    ("Shadow Exit", 120, 150, "shadow mode starts no earlier than day 100", "Anne Kessler"),
    ("Model-Risk Approval", 140, 190, "evidence pack format agreed", "Priya Natarajan"),
    ("Live Stable", 180, 230, "first release day 150 to 200, then 30 stable days", "Daniel Reyes"),
]
PROMISED_LIVE = 150   # "live in production in under five months"


def main():
    print("REBASELINE  Caldwell Mutual  day 12")
    print(f"  {'gate':<21}{'deal sheet':>11}{'field est.':>11}{'re-baselined':>14}  depends on (owner)")
    for g, d, f, (_, lo, hi, dep, who) in zip(GATES, DEAL_SHEET, FIELD_ESTIMATE, REBASELINED):
        print(f"  {g:<21}{d:>11}{f:>11}{f'{lo}-{hi}':>14}  {dep} ({who})")
    lo, hi = REBASELINED[-1][1], REBASELINED[-1][2]
    print(f"promised: live in under five months (day {PROMISED_LIVE}); re-baselined Live Stable: day {lo} to {hi}; "
          f"field estimate: day {FIELD_ESTIMATE[-1]}")
    print(f"slip against the promise, stated on day 12: {lo - PROMISED_LIVE} to {hi - PROMISED_LIVE} days")
    b, s, m = DEAL_SHEET[1], DEAL_SHEET[2], DEAL_SHEET[3]
    print(f"deal sheet: Build Complete to Live Stable in {DEAL_SHEET[-1] - b} days "
          f"(field estimate {FIELD_ESTIMATE[-1] - FIELD_ESTIMATE[1]}, re-baselined "
          f"{REBASELINED[-1][1] - REBASELINED[1][2]} to {REBASELINED[-1][2] - REBASELINED[1][1]})")


if __name__ == "__main__":
    main()
