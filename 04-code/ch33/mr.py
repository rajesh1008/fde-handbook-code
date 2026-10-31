"""The chapter's modelrisk module: fieldkit's copy once promoted (v4.1), the chapter draft before that."""
import _paths  # noqa: F401
try:
    from fieldkit import modelrisk as M  # noqa: F401
except ImportError:  # before promotion
    import modelrisk as M  # noqa: F401
