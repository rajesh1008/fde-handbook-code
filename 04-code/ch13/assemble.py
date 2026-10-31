"""Assemble 02-manuscript/ch13.md from the drafts in _draft/, resolving lab placeholders so every
listing and output block in the chapter is the real file or the real run output:
  {{OUT:name}}            -> output/name.txt (captured by run_all)
  {{CODE:path:Symbol}}    -> source of a top-level function or class, or Class.method, via ast
  {{HEAD:path:N}}         -> first N lines of a file
Usage: python assemble.py
"""
import ast, pathlib, re
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]

def code(path, sym):
    src = (ROOT / path).read_text()
    tree = ast.parse(src)
    parts = sym.split(".")
    nodes = tree.body
    node = None
    for p in parts:
        node = next(n for n in nodes if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == p)
        nodes = node.body
    lines = src.splitlines()
    start = (node.decorator_list[0].lineno if node.decorator_list else node.lineno) - 1
    block = lines[start:node.end_lineno]
    ind = len(block[0]) - len(block[0].lstrip())
    return "\n".join(l[ind:] for l in block)

def resolve(m):
    kind, rest = m.group(1), m.group(2)
    if kind == "OUT":
        return (HERE / "output" / f"{rest}.txt").read_text().rstrip("\n")
    path, arg = rest.rsplit(":", 1)
    if kind == "CODE":
        return code(path, arg)
    return "\n".join((ROOT / path).read_text().splitlines()[: int(arg)])

text = "\n".join((HERE / "_draft" / f"p{i}.md").read_text().strip("\n") for i in (1, 2, 3, 4)) + "\n"
text = re.sub(r"\{\{(OUT|CODE|HEAD):([^}]+)\}\}", resolve, text)
assert "{{" not in text
(ROOT / "02-manuscript" / "ch13.md").write_text(text)
print("wrote 02-manuscript/ch13.md,", len(text.split()), "words")
