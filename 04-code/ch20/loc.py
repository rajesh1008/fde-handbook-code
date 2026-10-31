"""Listing 20.x: how much of the code is shared, counted from the files themselves."""
import _paths  # noqa: F401
import inspect, pathlib, io, tokenize
import adapters, suite
import fieldkit.estates, fieldkit.gateway


def code_lines(src):
    """Lines carrying code: no blanks, comments or docstrings."""
    lines = set()
    prev = tokenize.INDENT
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type == tokenize.STRING and prev in (tokenize.INDENT, tokenize.DEDENT, tokenize.NEWLINE, tokenize.NL):
            prev = tok.type
            continue
        if tok.type not in (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT,
                            tokenize.ENDMARKER):
            lines.update(range(tok.start[0], tok.end[0] + 1))
        prev = tok.type
    return len(lines)


core = {"suite.py": inspect.getsource(suite), "fieldkit/estates.py": inspect.getsource(fieldkit.estates),
        "fieldkit/gateway.py": inspect.getsource(fieldkit.gateway)}
shared = {"adapters.Port (shared plumbing)": inspect.getsource(adapters.Port)}
per = {"CaldwellAws": inspect.getsource(adapters.CaldwellAws), "GreystoneAzure": inspect.getsource(adapters.GreystoneAzure),
       "PennantGcp": inspect.getsource(adapters.PennantGcp)}
c = {k: code_lines(v) for k, v in core.items()}
s = {k: code_lines(v) for k, v in shared.items()}
p = {k: code_lines(v) for k, v in per.items()}
for k, v in {**c, **s}.items():
    print(f"core     {k:34s} {v:4d} lines")
for k, v in p.items():
    print(f"adapter  {k:34s} {v:4d} lines")
total = sum(c.values()) + sum(s.values()) + sum(p.values())
print(f"shared {sum(c.values()) + sum(s.values())} of {total} lines ({(sum(c.values()) + sum(s.values())) / total:.0%});"
      f" largest single adapter {max(p.values())} lines ({max(p.values()) / total:.0%})")
