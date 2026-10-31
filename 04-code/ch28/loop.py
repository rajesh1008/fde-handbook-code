"""Listing 28.6: the runaway lookup loop on an ambiguous patient match, without and with budgets and the breaker.
Deterministic stand-in: the tool, token counts and prices are simulated; the budget and breaker code is fieldkit's."""
import _paths  # noqa: F401
from fieldkit.guardrails import Budget, CircuitBreaker

PRICE_IN, PRICE_OUT = 3.00 / 1e6, 15.00 / 1e6  # stand-in prices per token for the drafting model
VARIANTS = [dict(name="Maria Lopez", dob="1961-04-12"), dict(name="Maria Lopez", dob="1961-04-12", clinic="downtown"),
            dict(name="Maria E. Lopez", dob="1961-04-12")]


def lookup(args):
    """Two records share the name and birth date (a merge Greystone's registration team has not finished)."""
    return ["GH0412871", "GH0412904"]


def agent(budget=None, breaker=None, cap=50, progress_rule="fewer candidates", show=False):
    calls, tokens, cost, seen_best, trace = 0, 0, 0.0, None, []
    stop = None
    for step in range(1, cap + 1):
        args = VARIANTS[(step - 1) % 3]
        if breaker and not breaker.allow("patient.lookup"):
            stop = "breaker open: 3 lookups without progress"
            break
        t_in, t_out = 2300 + 450 * (step - 1), 120
        if budget:
            why = budget.charge("patient.lookup", args, tokens=t_in + t_out, cost=t_in * PRICE_IN + t_out * PRICE_OUT)
            if why:
                stop = why
                break
        calls += 1; tokens += t_in + t_out; cost += t_in * PRICE_IN + t_out * PRICE_OUT
        found = lookup(args)
        if progress_rule == "fewer candidates":
            progress = len(found) == 1 or (seen_best is not None and len(found) < seen_best)
        else:  # "result changed": a weaker signal that counts any reordering as progress
            found = found if step % 2 else found[::-1]
            progress = trace == [] or found != trace[-1][2]
        seen_best = min(len(found), seen_best or 99)
        state = breaker.record("patient.lookup", progress) if breaker else "-"
        trace.append((step, args, found, progress, state, round(cost, 4)))
    else:
        stop = f"framework iteration cap ({cap}): exception, run ends with no handoff"
    return dict(calls=calls, tokens=tokens, cost=cost, stop=stop, trace=trace, seconds=calls * 1.8)


def show(name, r, n=None):
    print(f"\n{name}")
    for step, args, found, prog, state, _ in r["trace"][: n or len(r["trace"])]:
        a = ", ".join(f"{k}={v}" for k, v in args.items())
        print(f"  call {step:>2}  patient.lookup({a}) -> {len(found)} records  progress={'yes' if prog else 'no'}  breaker={state}")
    if n and len(r["trace"]) > n:
        print(f"  ... {len(r['trace']) - n} more calls of the same three variants")
    print(f"  stopped: {r['stop']}")
    print(f"  cost line: {r['calls']} tool calls, {r['tokens']:,} tokens, ${r['cost']:.2f}, {r['seconds']:.0f} s of wall clock")


if __name__ == "__main__":
    naive = agent()
    show("without budgets (the framework's default cap of 50 iterations)", naive, n=4)
    guarded = agent(Budget(max_steps=12, max_tool_calls=20, max_repeat=2, max_tokens=60_000, max_cost=0.40), CircuitBreaker(3))
    show("with Greystone's budgets B-01 to B-05 and breaker B-07", guarded)
    print("  route: referral to the coordinator queue with both candidate records and the reason; no draft")
    print("\ncumulative cost by call, without budgets: " + " ".join(f"{t[5]:.4f}" for t in naive["trace"]))
    print(f"\nwhat the budgets saved on one referral: {naive['calls'] - guarded['calls']} calls, ${naive['cost'] - guarded['cost']:.2f}")
    print(f"a bad registration merge touching 9 referrals in an hour: ${9 * naive['cost']:.2f} without budgets, ${9 * guarded['cost']:.2f} with them")
