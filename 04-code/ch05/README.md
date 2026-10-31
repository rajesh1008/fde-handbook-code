# Chapter 5 lab: three homes for the role

Plain Python 3.10+, no third-party packages (pytest for the tests). There are no model calls. The lab is
comparison data and arithmetic, so the deterministic stand-in convention is not needed. It imports
`fieldkit` 0.1.0 unchanged (fixtures and version check) and the Chapter 2 lab (`04-code/ch02`) for the
vendor's cost of one more month. All money is US dollars. Every figure is illustrative and belongs to
the fictional Northlight AI, its customers, and the chapter's model of each home. None of it is a survey of
any company.

| File | What it does | Output |
|---|---|---|
| `homes.py` | Listing 5.1: three Home records (fixed point, pay, tax payer, reuse route, exit, incentives, assets) | `output/homes.txt` |
| `economics.py` | Listing 5.2: who pays 840 integration hours, and one more month, in each home | `output/economics.txt` |
| `playbook.py` | Listing 5.3: plays with required assets and assumed incentives; `fit()` gives OK, BENT, BREAKS, INVERTS | `output/playbook.txt` |
| `failure_vendor_playbook_at_integrator.py` | Listing 5.4: failure injection, Northlight's vendor playbook run by an integrator, then the repair | `output/failure_vendor_playbook_at_integrator.txt` |
| `reuse.py` | Listing 5.5: six field fixes routed three ways, with what closes each | `output/reuse.txt` |
| `disagreements.py` | Listing 5.7: the first-month disagreement log of the two new hires | `output/disagreements.txt` |
| `customer_view.py` | Listing 5.6: the customer's five questions, by home | `output/customer_view.txt` |
| `choose.py` | Listing 5.8: weighted home scores and the six questions for a prospective employer | `output/choose.txt` |
| `tryit.py 1/2/3` | Try It Yourself variations | `output/try_N.txt` |
| `test_ch05.py` | 12 tests that pin every number the chapter prints | `output/tests.txt` |

Run everything:

```
bash make_outputs.sh
```

Illustrative assumptions are labeled in `economics.py`: an integrator bill rate of 240 dollars an hour,
a lab carrying 25% of the integration hours itself, and lab consumption of 40,000 dollars a month once in production.
