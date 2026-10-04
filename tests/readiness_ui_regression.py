import ast
from pathlib import Path
src=Path("app.py").read_text()
ast.parse(src)
assert 'Use model readiness targets' in src
assert '_READINESS=' in src
assert 'week>=4' in src and 'week>=7' in src
assert 'Measured autonomous reliability' in src
print("Readiness UI regression passed.")
