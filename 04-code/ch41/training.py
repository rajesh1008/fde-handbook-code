"""Training by competence check: share of tasks each cohort did alone, by session."""
import world as W
print("share of tasks done alone (a), assisted (s), not yet (n)")
for cohort, sessions in W.TRAIN.items():
    for day, s in zip(W.TRAIN_DAYS, sessions):
        print(f"{cohort:<30}day {day}  alone {s.count('a')}/{len(s)} = {s.count('a') / len(s):.2f}  assisted {s.count('s')}")
for cohort, sessions in W.TRAIN.items():
    left = [t for t, c in zip(W.TRAIN_TASKS[cohort], sessions[-1]) if c != "a"]
    print(f"{cohort}: not yet alone after session 4: {', '.join(left) or 'none'}")
