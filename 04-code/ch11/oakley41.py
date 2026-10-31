"""Sam Oakley's 41 questions (day 5): theme, whether the answer can change the design, status by day 40."""
THEMES = [  # theme, count, design-changing, answered by day 40
    ("data flow and storage", 9, 7, 3),
    ("access and identity", 8, 6, 3),
    ("logging and audit", 6, 4, 2),
    ("model behavior and output", 6, 4, 1),
    ("incident and breach", 4, 1, 1),
    ("retention and deletion", 4, 1, 1),
    ("subprocessors and contracts", 4, 0, 0),
]
QUESTIONS = []
n = 1
for theme, count, design, answered in THEMES:
    for i in range(count):
        QUESTIONS.append(dict(id=f"SQ-{n:02d}", theme=theme, design=i < design, answered40=i < answered))
        n += 1

def summary():
    lines = ["Sam Oakley's questions, asked day 5", f"  {'theme':<28}{'asked':>6}{'design':>8}{'answered d40':>14}"]
    for theme, count, design, answered in THEMES:
        lines.append(f"  {theme:<28}{count:>6}{design:>8}{answered:>14}")
    t = len(QUESTIONS); d = sum(q['design'] for q in QUESTIONS); a = sum(q['answered40'] for q in QUESTIONS)
    lines.append(f"  {'total':<28}{t:>6}{d:>8}{a:>14}")
    lines.append(f"  {d} of {t} answers can change the design; asked at sign-off, each one is rework")
    return "\n".join(lines)
