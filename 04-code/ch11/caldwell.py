"""Caldwell Mutual: map at day 25 and the architect review fixture."""
from stakeholders import Person, StakeholderMap

DAY25 = StakeholderMap("Caldwell", 25, [
    Person("reyes", "Daniel Reyes", "CTO", ("sponsor",), 23, source="own words"),
    Person("kessler", "Anne Kessler", "Head of Claims", ("owner", "approver"), 24, source="own words"),
    Person("natarajan", "Priya Natarajan", "Enterprise architect", ("approver",), 22, source="own words"),
    Person("whitfield", "Tom Whitfield", "Senior adjuster", ("operator",), 19, source="observed"),
    Person("calloway", "Ruth Calloway", "Claims data manager", ("owner",), 24, champion=True, source="observed"),
])

# Architecture review requests sent to Priya Natarajan, by what was sent, and days to a written answer.
REVIEWS = {
    "decision record": [1, 2, 2, 1, 3, 2, 4],
    "diagram with notes": [3, 4, 5, 4, 3, 6],
    "slide deck": [8, 9, 12, 7, 10],
}
