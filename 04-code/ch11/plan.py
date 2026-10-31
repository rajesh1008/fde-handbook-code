"""Two Greystone plans. Stand-in estimates, labelled as such: the durations are planning assumptions, not measurements."""
import oakley41

DESIGN_CHANGING = sum(q["design"] for q in oakley41.QUESTIONS)

def signoff_plan():
    build_end = 105                     # build without security input
    review = 30                         # first full review of 41 questions at the end
    rework = round(DESIGN_CHANGING * 1.5)   # stand-in: 1.5 working days per design-changing finding
    rereview = 10
    phases = [("build", 20, build_end), ("security review", build_end, build_end + review),
              ("rework", build_end + review, build_end + review + rework),
              ("re-review", build_end + review + rework, build_end + review + rework + rereview)]
    return phases, phases[-1][2]

def design_plan():
    clinic_cost = round(DESIGN_CHANGING * 0.25)   # stand-in: a quarter day each when found in a clinic
    build_end = 105 + clinic_cost + 1
    phases = [("build", 20, build_end), ("security clinics", 30, 41),
              ("final review", build_end, build_end + 14), ("buffer", build_end + 14, build_end + 28)]
    return phases, phases[-1][2]

def report():
    a, pa = signoff_plan(); b, pb = design_plan()
    lines = [f"Stand-in plan model, {DESIGN_CHANGING} design-changing questions"]
    for name, ph, end in (("approvers at sign-off", a, pa), ("approvers at design", b, pb)):
        lines.append(f"  {name}: pilot projected day {end}")
        for p, s, e in ph:
            lines.append(f"    {p:<17} day {s:>3} to {e:>3}")
    lines.append(f"  difference: {pa - pb} days, about ${(pa - pb) / 30 * 235_500:,.0f} at the slip cost of $235,500 a month")
    return "\n".join(lines)
