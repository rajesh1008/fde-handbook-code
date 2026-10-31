"""The customer's view of the three homes: five questions a buyer asks of any FDE.

Risk to the customer: 0 low, 1 medium, 2 high (the chapter's model, not a survey).
"""
QUESTIONS = [
    ("who answers at 2 a.m.", {"vendor": ("vendor product support", 0),
                               "integrator": ("run service if bought, else the customer", 1),
                               "lab": ("the customer's team or a partner", 2)}),
    ("who owns what was built", {"vendor": ("vendor owns product; customer owns config", 1),
                                 "integrator": ("customer, by contract", 0),
                                 "lab": ("customer owns the app; lab owns the model", 1)}),
    ("what leaving costs", {"vendor": ("re-platform off the product", 2),
                            "integrator": ("knowledge transfer from the integrator", 1),
                            "lab": ("re-prompt and re-evaluate on another model", 1)}),
    ("whose incentive is duration", {"vendor": ("vendor wants it short", 0),
                                     "integrator": ("integrator earns from length", 2),
                                     "lab": ("lab wants consumption soon", 0)}),
    ("who holds acceptance", {"vendor": ("customer's experts, if the contract says so", 1),
                              "integrator": ("customer, by statement of work", 0),
                              "lab": ("often the lab's own evals", 2)}),
]


def totals():
    t = {"vendor": 0, "integrator": 0, "lab": 0}
    for _, row in QUESTIONS:
        for k, (_, r) in row.items():
            t[k] += r
    return t


def main():
    print("THE CUSTOMER'S VIEW  (risk to the customer: 0 low, 1 medium, 2 high)")
    for q, row in QUESTIONS:
        print(f"  {q}")
        for k, (a, r) in row.items():
            print(f"      {k:<11}{r}  {a}")
    t = totals()
    print("  total risk (of 10): " + "  ".join(f"{k} {v}" for k, v in t.items()))
    print("  no home is lowest on every question; the buyer picks which risk to carry")


if __name__ == "__main__":
    main()
