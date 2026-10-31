"""Greystone's architecture and control clinic: every item ends as an approved decision or a dated owner action."""
from cadence_data import GREYSTONE_CLINIC
from fieldkit.deployment import is_person

def problems(row):
    key, q, by, day, outcome, owner, due = row
    if outcome == "decision" and is_person(owner):
        return None
    if outcome == "action" and is_person(owner) and due:
        return None
    return "left the room without a decision or a dated owner action"

def main():
    print("ARCHITECTURE AND CONTROL CLINIC  Greystone Health  days 30-40 (4 sessions)")
    for row in GREYSTONE_CLINIC:
        key, q, by, day, outcome, owner, due = row
        p = problems(row)
        tail = f"decision ({owner})" if outcome == "decision" else (
            f"action {owner} by day {due}" if outcome == "action" else "NO OUTCOME")
        print(f"  day {day}  {key}  {tail:<32}{q}")
        if p:
            print(f"           FLAG  {p}")
    n = len(GREYSTONE_CLINIC)
    d = sum(r[4] == "decision" for r in GREYSTONE_CLINIC)
    a = sum(r[4] == "action" for r in GREYSTONE_CLINIC)
    print(f"items {n}: decisions {d}, dated actions {a}, flagged {n - d - a}; "
          f"questions from the security list with an outcome: {d + a} of 41")

if __name__ == "__main__":
    main()
