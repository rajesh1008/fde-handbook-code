"""Figure 18.5: each gateway response class and the one action the adapter takes for it."""
from _common import S, save, blank
from fieldkit.gateway import ACTIONS
SHORT = {"auth": "refresh key, retry once, then page", "allowlist": "stop; ticket to network owner",
         "rate_limited": "wait Retry-After, retry", "content_filtered": "no retry; route to a person",
         "retired": "stop; move to successor", "bad_request": "stop; contract test missed it",
         "server": "back off, retry in budget"}
fig, ax = S.figure(height=4.6)
blank(ax, (0, 10), (0, 7.4))
codes = {"auth": "401", "allowlist": "403", "rate_limited": "429", "content_filtered": "400 filter",
         "retired": "404/410", "bad_request": "other 4xx", "server": "5xx"}
role = {"auth": "data", "allowlist": "blocker", "rate_limited": "cost", "content_filtered": "approval",
        "retired": "blocker", "bad_request": "blocker", "server": "system"}
for i, (k, a) in enumerate(ACTIONS.items()):
    y = 6.4 - i * 0.95
    S.box(ax, 0.1, y, 1.4, 0.75, codes[k], role=role[k], fs=10, mono=True)
    S.arrow(ax, 1.5, y + 0.37, 1.9, y + 0.37)
    S.label(ax, 2.0, y + 0.37, SHORT[k], fs=10, va="center")
save(fig, 5, kind="diagram", data="04-code/fieldkit/fieldkit/gateway.py ACTIONS")
