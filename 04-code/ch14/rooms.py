"""Listing 14.1b driver: the question bank by room, four parts per question, with day-by-day status."""
import question_bank as qb


def main():
    for room in ("Michael", "Sam"):
        rows = [q for q in qb.BANK if q.room == room]
        print(f"{room}'s room: {len(rows)} questions, {sum(q.blocking for q in rows)} blocking")
    print()
    for key in ("M05", "S05", "M14"):
        q = next(x for x in qb.BANK if x.key == key)
        print(f"{q.key} {q.text}\n   why:      {q.why}\n   expected: {q.expected}\n   edge:     {q.edge}\n"
              f"   answer:   {q.answer} ({q.answered_by}, day {q.day_answered}; {q.status})")
    print()
    print("Not answered by day 19:", "; ".join(f"{q.key} {q.text}" for q in qb.BANK if q.day_answered is None))
    t = qb.tally(qb.BANK, 19)
    print("Statuses of answers:", ", ".join(f"{k} {v}" for k, v in t["by_status"].items()))


if __name__ == "__main__":
    main()
