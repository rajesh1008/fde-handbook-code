"""Failure injection: a customer change freeze that blocks a security fix (Greystone, production month 9).

The managed-service provider freezes changes for the EHR upgrade, days 440 to 461. On day 443 a critical advisory
lands for the attachment parser on the fax-referral path. Greystone's policy (Sam Oakley): critical fixes live within
14 days. v0 files the fix as a standard change and waits; v1 runs the conflict check every morning and applies the
mode rule. Deterministic stand-in: the day arithmetic is real, the volumes and minutes are the lab's.
"""
import sys
import _paths  # noqa: F401

FREEZE = (440, 461)
ADVISORY_DAY, ADVISORY_MIN = 443, 9 * 60 + 10      # read from the feed at 09:10
POLICY_DAYS = 14
BOARD_DAYS = (1, 4)                                   # change board twice weekly: day % 7 in these
STANDARD_LEAD = 3                                     # standard change: three working days after approval
REFERRALS_A_DAY = 415
FAX_SHARE = 0.34                                      # share of referrals arriving as fax attachments
MANUAL_MIN = 6.5                                      # extra coordinator minutes per referral done by hand


def frozen(d, freeze=FREEZE):
    return freeze[0] <= d <= freeze[1]


def next_board(d):
    while d % 7 not in BOARD_DAYS:
        d += 1
    return d


def working_days_after(d, n):
    while n:
        d += 1
        if d % 7 not in (5, 6):
            n -= 1
    return d


def v0(freeze=FREEZE, policy=POLICY_DAYS):
    """The fix is ready on day 445 and filed as a standard change; the calendar rejects it while frozen."""
    ready = ADVISORY_DAY + 2
    board = next_board(max(ready, freeze[1] + 1))
    live = working_days_after(board, STANDARD_LEAD)
    due = ADVISORY_DAY + policy
    weekly = next(d for d in range(ADVISORY_DAY, 600) if d % 7 == 3 and d > due)   # Sam Oakley's weekly report
    return dict(ready=ready, board=board, live=live, due=due, exposure_days=live - ADVISORY_DAY,
                past_policy=max(0, live - due), breach_seen=weekly, manual_referrals=0, manual_hours=0.0)


def conflict(freeze=FREEZE, policy=POLICY_DAYS):
    """The v1 morning check: a security clock whose normal path lands after its due day, or inside a freeze."""
    due = ADVISORY_DAY + policy
    normal = v0(freeze, policy)["live"]
    return (normal > due or frozen(due, freeze)), due, normal


def v1(freeze=FREEZE, policy=POLICY_DAYS, emergency=True):
    hit, due, normal = conflict(freeze, policy)
    mitig_min = ADVISORY_MIN + 150                      # mode M3 "fax attachments to manual intake", 2.5 hours
    if not hit:
        return dict(conflict=False, live=normal, due=due)
    if emergency:
        filed = ADVISORY_DAY + 1                        # evidence pack: patched parser on the 300 packets
        approved = next_board(filed + 1)                # emergency board: provider change manager, Sam Oakley,
        live = approved + 1                             # Denise Alvarez; deploy 02:00 outside clinic hours
    else:
        filed = approved = None
        live = normal
    manual_days = live - ADVISORY_DAY
    refs = round(REFERRALS_A_DAY * FAX_SHARE * manual_days)
    return dict(conflict=True, due=due, normal=normal, mitigated_min=mitig_min, filed=filed, approved=approved,
                live=live, exposure_hours=round((mitig_min - ADVISORY_MIN) / 60, 1), patch_days=live - ADVISORY_DAY,
                past_policy=max(0, live - due), manual_days=manual_days, manual_referrals=refs,
                manual_hours=round(refs * MANUAL_MIN / 60, 1))


def hhmm(m):
    return f"{m // 60:02d}:{m % 60:02d}"


def show_v0():
    r = v0()
    print("FREEZE v0  Greystone, production month 9  (deterministic stand-in)")
    print(f"  freeze days {FREEZE[0]}-{FREEZE[1]} (EHR upgrade, managed-service provider calendar)")
    print(f"  day {ADVISORY_DAY} 09:10  critical advisory: attachment parser on the fax-referral path")
    print(f"  day {r['ready']}        fix built; evaluation suite passes; filed as a STANDARD change")
    print(f"  day {r['ready']}        provider calendar: REJECTED, window frozen until day {FREEZE[1]}; requeued")
    print(f"  day {r['due']}        policy due (critical within {POLICY_DAYS} days): fix not live")
    print(f"  day {r['breach_seen']}        Sam Oakley's weekly report shows the breach; the request is still queued")
    print(f"  day {r['board']}        first change board after the freeze approves it")
    print(f"  day {r['live']}        fix live")
    print(f"  exposure {r['exposure_days']} days, {r['past_policy']} days past policy; fax path open throughout")
    return r


def show_v1():
    r = v1()
    print("FREEZE v1  same calendar, conflict check every morning, mode rule  (deterministic stand-in)")
    print(f"  day {ADVISORY_DAY} 09:10  advisory read; conflict check: due day {r['due']}, normal path live day "
          f"{r['normal']} -> CONFLICT")
    print(f"  day {ADVISORY_DAY} {hhmm(r['mitigated_min'])}  mode M3 on: fax attachments to manual intake "
          f"(pre-approved operating mode, not a change); exposure {r['exposure_hours']} h")
    print(f"  day {r['filed']}        emergency change filed with evidence: patched parser on Tess Moreno's 300 "
          f"packets, 300 of 300 identical")
    print(f"  day {r['approved']}        emergency board approves: provider change manager, Sam Oakley, Denise Alvarez")
    print(f"  day {r['live']} 02:00  fix live outside clinic hours; smoke test; mode M3 off at 07:00")
    print(f"  patch {r['patch_days']} days after the advisory, {r['past_policy']} days past policy")
    print(f"  cost: {r['manual_days']} days of manual fax intake, {r['manual_referrals']} referrals, "
          f"{r['manual_hours']} coordinator hours")
    print("OPTIONS")
    w = v0(); m = v1(emergency=False); e = r
    print(f"  {'option':<38}{'exposure':>12}{'past policy':>13}{'manual referrals':>18}{'hours':>8}")
    print(f"  {'wait for the freeze to end (v0)':<38}{str(w['exposure_days']) + ' d':>12}{w['past_policy']:>13}"
          f"{0:>18}{0:>8}")
    print(f"  {'manual mode until the freeze ends':<38}{str(m['exposure_hours']) + ' h':>12}{m['past_policy']:>13}"
          f"{m['manual_referrals']:>18}{m['manual_hours']:>8}")
    print(f"  {'manual mode plus emergency change (v1)':<38}{str(e['exposure_hours']) + ' h':>12}"
          f"{e['past_policy']:>13}{e['manual_referrals']:>18}{e['manual_hours']:>8}")
    print("  note: in option 2 the fix still lands after policy; manual mode closes the exposure, not the finding")
    return r


if __name__ == "__main__":
    (show_v1 if (len(sys.argv) > 1 and sys.argv[1] == "v1") else show_v0)()
