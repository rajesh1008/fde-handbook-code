"""Mid-sprint playback at Caldwell, sprint 2 day 7 (engagement day 49): run on the first real traces,
with the operator in the room, and decide what changes in the second half of the sprint."""
from cadence_data import caldwell_sprint2

TRACE_FINDINGS = [   # from the 200 documents that arrived on day 47 (readiness register, Chapter 15)
    ("policy_number filled", 0.975, 0.98, "C-03"),
    ("OCR confidence >= 0.80", 0.765, 0.80, "C-05"),
]

def main():
    items = {i.key: i for i in caldwell_sprint2()}
    print("MID-SPRINT PLAYBACK  Caldwell Mutual  sprint 2  day 49 (sprint day 7)")
    print("  shown on: 200 real documents from day 47, traces replayed, Anne Kessler and Tom Whitfield present")
    changes = []
    for what, seen, need, key in TRACE_FINDINGS:
        flag = "below" if seen < need else "meets"
        print(f"  {what:<26}{seen:.1%} vs {need:.0%}  {flag}  -> {key} {items[key].title}")
        if seen < need:
            changes.append(key)
    print("second half of the sprint:")
    print("  C-03 acceptance criterion kept; policy_number reported as its own line, not averaged in")
    print("  C-05 hold threshold confirmed at 0.80; held batches go to the readiness report, not the queue")
    print("  C-04 at risk: D-05 (adjuster SSO group) open 19 days; Tom cannot test under his own identity")
    print(f"items changed: {len(changes)}  criteria lowered: 0  items added: 0")

if __name__ == "__main__":
    main()
