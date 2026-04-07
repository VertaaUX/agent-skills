# Contributing

Thanks for improving the VertaaUX agent skills repository.

## Scope

This repository is documentation-first. Most changes will touch:

- `README.md`
- `skills/vertaaux/SKILL.md`
- `skills/vertaaux/references/*.md`
- GitHub automation and repository hygiene under `.github/`

## Contribution Guidelines

- Keep claims aligned with real VertaaUX behavior. Do not add undocumented CLI flags, API parameters, or workflow guarantees.
- Prefer small, reviewable pull requests.
- Preserve or improve link accuracy when moving or renaming docs.
- Update examples when a reference or command changes.
- Use plain, copy-pasteable shell examples where possible.

## Local Review Checklist

Before opening a pull request:

1. Confirm all relative Markdown links still resolve.
2. Confirm the README still matches the repository layout.
3. Verify any new command examples are consistent with the referenced VertaaUX surfaces.
4. Run the same repository checks used in CI:

```bash
python3 - <<'PY'
from pathlib import Path
import re

root = Path(".")
files = [root / "README.md", root / "skills/vertaaux/SKILL.md", *sorted((root / "skills/vertaaux/references").glob("*.md"))]
pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
errors = []

for file in files:
    text = file.read_text()
    for target in pattern.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        path = target.split("#", 1)[0]
        if not (file.parent / path).exists():
            errors.append(f"{file}: missing link target {target}")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)

print("Markdown links look valid.")
PY
```

## Pull Requests

PRs should explain:

- what changed
- why the change improves the skill or repository
- any follow-up work still left open

When updating skill behavior, include the affected file paths and call out any examples that were revised.
