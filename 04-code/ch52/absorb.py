"""Listing 52.6: who does each piece of Caldwell's engagement work in 2026, and the chapter's forecast for 2029.

The 2029 column is a forecast written by this chapter, not a measurement. Owners: product (Northlight ships it),
playbook (a written, repeatable procedure a less senior person runs), FDE (judgment in the customer's building).
"""
WORK = [  # (work item, chapter, 2026 owner, 2029 forecast, reason it stays or moves)
    ("model gateway adapter", 18, "playbook", "product", "interface"),
    ("document connectors to the claims system", 19, "FDE", "product", "interface"),
    ("synthetic document generator", 16, "playbook", "product", "tooling"),
    ("prompt and rule packaging", 24, "FDE", "product", "tooling"),
    ("evaluation suite runner", 26, "playbook", "product", "tooling"),
    ("router calibration refit", 27, "FDE", "product", "tooling"),
    ("cost and latency dashboards", 30, "playbook", "product", "tooling"),
    ("deprecation register and candidate rerun", 42, "FDE", "product", "tooling"),
    ("trace and evidence pack assembly", 40, "playbook", "product", "tooling"),
    ("observability and alert routing", 42, "product", "product", "tooling"),
    ("access tracker", 15, "playbook", "product", "tooling"),
    ("security questionnaire answers", 32, "FDE", "playbook", "repeatable"),
    ("shadow runner setup", 39, "FDE", "playbook", "repeatable"),
    ("rollback drill", 41, "FDE", "playbook", "repeatable"),
    ("runbooks and on-call rota", 42, "FDE", "playbook", "repeatable"),
    ("pricing the engagement", 46, "FDE", "playbook", "repeatable"),
    ("statement of work and gates", 37, "playbook", "playbook", "repeatable"),
    ("training the customer's operators", 41, "FDE", "playbook", "repeatable"),
    ("test pyramid configuration", 29, "FDE", "playbook", "repeatable"),
    ("discovery with the claims handlers", 6, "FDE", "FDE", "tacit knowledge"),
    ("gold set built with the customer's expert", 26, "FDE", "FDE", "accountability"),
    ("deciding what counts as critical", 26, "FDE", "FDE", "accountability"),
    ("sponsor and stakeholder map", 11, "FDE", "FDE", "politics"),
    ("negotiating a gate the customer owns", 37, "FDE", "FDE", "accountability"),
    ("model-risk validation conversation", 33, "FDE", "FDE", "accountability"),
    ("choosing deterministic over model", 9, "FDE", "FDE", "judgment"),
    ("the first incident with the customer in the room", 42, "FDE", "FDE", "judgment"),
    ("hand-over readiness and walking away", 41, "FDE", "FDE", "judgment"),
    ("reading a new model's behavior change", 52, "FDE", "FDE", "judgment"),
    ("stopping a deal that will not go live", 8, "FDE", "FDE", "judgment"),
]

if __name__ == "__main__":
    print(f"Caldwell engagement work items: {len(WORK)}")
    print(f"{'owner':<10}{'2026':>6}{'2029 forecast':>15}")
    for o in ("product", "playbook", "FDE"):
        print(f"{o:<10}{sum(w[2] == o for w in WORK):>6}{sum(w[3] == o for w in WORK):>15}")
    moved = [w for w in WORK if w[2] != w[3]]
    print(f"moves between 2026 and 2029: {len(moved)}; FDE to product: "
          f"{sum(w[2] == 'FDE' and w[3] == 'product' for w in moved)}; FDE to playbook: "
          f"{sum(w[2] == 'FDE' and w[3] == 'playbook' for w in moved)}")
    print("stays with the FDE in the forecast, by reason:")
    reasons = {}
    for w in WORK:
        if w[3] == "FDE":
            reasons.setdefault(w[4], []).append(w[0])
    for r, items in reasons.items():
        print(f"  {r:<16}{len(items)}: {'; '.join(items)}")
