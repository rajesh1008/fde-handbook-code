# Chapter 1 lab: where did the week go?

Parses one week of calendar, tickets and commits into a time-allocation table filed under the six verbs
of the job (discover, decide, access, build, pass, hand over) plus internal and travel, and gives a
deterministic verdict. No model is called. Uses the current `fieldkit` (customer fixtures and the
Caldwell access tracker, which says on which days the model gateway key rotates).

## Run

```bash
python make_weeks.py            # writes the fixture weeks into data/ (deterministic)
python weeklog.py               # all reports; or: a | b | compare | greystone
python -m pytest -q test_weeklog.py
```

Captured output lives in `output/`: `week_a.txt`, `week_b.txt`, `compare.txt`, `greystone.txt`, `pytest.txt`.

## Inputs

| File | Columns | Note |
|---|---|---|
| `data/<week>_calendar.csv` | day, start, end, title, attendees, tag | The only source of hours. Focus blocks are calendar events. |
| `data/<week>_tickets.csv` | id, opened_day, closed_day, title, owner, tag | Counted as evidence; an item "moved" if opened or closed this week. |
| `data/<week>_commits.log` | hash \| day N \| author \| subject \| path | Counted per verb from the path prefix. |

## Weeks

* `week_a_caldwell`: days 81 to 85 at Caldwell Mutual. Day 82 is the Tuesday in section 1.1 and a key-rotation day.
* `week_b_injected`: failure injection. Days 88 to 92, every customer meeting cancelled, 41 commits, 19 tickets closed, zero customer contact, and a key rotation on day 89 nobody checked.
* `week_c_greystone`: the second customer. Greystone Health's infrastructure staff sit on a managed-service provider's domain, so a one-domain contact rule undercounts.

## Rules

* Customer contact = calendar hours with anyone from a customer domain in attendance.
* Flags: contact share below 15%; nothing customer-owned moved; any of the six verbs untouched; a gateway key rotation day with no access event.
* `PRODUCTIVE-LOOKING` fires when commits are at least 1.5x the baseline week, contact is under 15% and nothing the customer owns moved.

## Try It Yourself

1. **Move the threshold.** Set `MIN_CONTACT_SHARE` to 0.30 and rerun. Week A flips to CHECK at 29%. Decide, in writing, what share your engagements actually need and why, before you look at your own numbers.
2. **Your own week.** Export last week's calendar to the CSV columns above, tag each event with one bucket, and run `weeklog.load` on it. The untagged events you could not file are the finding.
3. **Second customer.** Run `python weeklog.py greystone`, then add a third domain for a contractor you work with and see how the contact share and the verdict change. Note that `discover` stays untouched either way: domains fix the count, not the week.
