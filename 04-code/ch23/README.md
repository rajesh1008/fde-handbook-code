# Chapter 23 lab: RAG on Caldwell's claims policy library

Deterministic stand-in. Nothing here is Caldwell data: the library (713 files, 6,452 passages), its ACLs, the
four-version water-loss section CM-WL-07, Anne Kessler's 150 questions and every rate are generated or assumed so
that each number in the chapter re-runs exactly. Run `./make_outputs.sh` (uses `/workspace/books/.venv`).

| Listing | File | Output | Section |
|---|---|---|---|
| 23.1 | `store_options.py` | `output/store_options.txt` | 23.1 Whose embeddings, whose store |
| 23.2 | `acl_inherit.py` | `output/acl_inherit.txt` | 23.2 Access control inherited from the source (failure injection 1) |
| 23.3 | `acl_drift.py` | `output/acl_drift.txt` | 23.2 ACL drift and sync cadence |
| 23.4 | `supersession.py` | `output/supersession.txt` | 23.3 Freshness and supersession (failure injection 2) |
| 23.5 | `evaluate.py` | `output/evaluate.txt` | 23.4 Measuring retrieval with the customer's questions |
| 23.6 | `cost.py` | `output/cost.txt` | 23.5 Cost attribution |
| 23.7 | `../fieldkit/fieldkit/retrieval.py` | `output/tests.txt` | 23.7 fieldkit v3 |
| Try It | `tryit.py a|b|c` | `output/tryit.txt` | Try It Yourself |

`caldwell_docs.py` builds the library and the question set from seed 23. The embedding is a stand-in for the
Caldwell gateway's embedding deployment: it knows about 80% of the adjusters' phrasings and none of the identifiers.
