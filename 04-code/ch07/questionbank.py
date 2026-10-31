"""Shim: use fieldkit's question bank when installed (Chapter 7 promotes it), else the local copy."""
try:
    from fieldkit.questionbank import *  # noqa: F401,F403
    from fieldkit.questionbank import Bank, Question, Answer, Reconciliation, acting_for_gaps, coverage, STATUSES  # noqa: F401
except ImportError:
    from questionbank_impl import *  # noqa: F401,F403
    from questionbank_impl import Bank, Question, Answer, Reconciliation, acting_for_gaps, coverage, STATUSES  # noqa: F401
