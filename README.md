# bitranox_template_py_lib

<!-- Badges -->
[![CI](https://github.com/bitranox/bitranox_template_py_lib/actions/workflows/default_cicd_public.yml/badge.svg)](https://github.com/bitranox/bitranox_template_py_lib/actions/workflows/default_cicd_public.yml)
[![CodeQL](https://github.com/bitranox/bitranox_template_py_lib/actions/workflows/codeql.yml/badge.svg)](https://github.com/bitranox/bitranox_template_py_lib/actions/workflows/codeql.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Open in Codespaces](https://img.shields.io/badge/Codespaces-Open-blue?logo=github&logoColor=white&style=flat-square)](https://codespaces.new/bitranox/bitranox_template_py_lib?quickstart=1)
[![PyPI](https://img.shields.io/pypi/v/bitranox_template_py_lib.svg)](https://pypi.org/project/bitranox_template_py_lib/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/bitranox_template_py_lib.svg)](https://pypi.org/project/bitranox_template_py_lib/)
[![Code Style: Ruff](https://img.shields.io/badge/Code%20Style-Ruff-46A3FF?logo=ruff&labelColor=000)](https://docs.astral.sh/ruff/)
[![codecov](https://codecov.io/gh/bitranox/bitranox_template_py_lib/graph/badge.svg?token=UFBaUDIgRk)](https://codecov.io/gh/bitranox/bitranox_template_py_lib)
[![Maintainability](https://qlty.sh/badges/041ba2c1-37d6-40bb-85a0-ec5a8a0aca0c/maintainability.svg)](https://qlty.sh/gh/bitranox/projects/bitranox_template_py_lib)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

A scaffold for backward-compatible (Python 3.9+) libraries that ship a registered CLI command,
with a rich-click entry point, strict typing, and a full test-and-release pipeline already wired.

## Why a template

Starting a new Python library feels like it should be about the library. It almost never is.
The first day goes on the scaffolding nobody brags about: which linter, which type checker, how
the version number stays in step across three files, how a tag becomes a PyPI release, which
Python versions you have quietly promised to keep working. None of that is the thing you set out
to build, and all of it has to be right before the thing you set out to build can ship.

The tax on that work is invisible, which is exactly why people underprice it. A blank directory
looks free. It is not. It is a stack of small decisions you will make in a hurry, slightly
wrong, and then copy by hand into the next project, where you will make them slightly wrong
again. A blank page is not a fresh start so much as a bill you have agreed to pay later.

A template is the boring answer that settles the bill up front. You inherit a working set of
defaults, tests green across six Python versions and three operating systems, strict typing, a
lint/type/test/release pipeline behind a single `make` command, a CLI that already runs, so the
only decisions left are the ones that are actually about your library. The point is not that
these are the only good choices. The point is that they are already made and already wired
together, so you get to disagree with one on purpose rather than rediscover all of them by
accident.

So clone it, delete the parts you do not want, and spend day one on the problem you actually
care about. That is the whole trick: make the sensible path the lazy one.

## Quickstart

Install from PyPI (uv recommended, plain `pip` works too):

```bash
uv pip install bitranox_template_py_lib
```

Run the CLI:

```bash
bitranox_template_py_lib hello     # -> Hello World
bitranox_template_py_lib info      # print resolved package metadata
bitranox_template_py_lib --help
```

Or run it without installing:

```bash
uvx bitranox_template_py_lib hello
python -m bitranox_template_py_lib hello
```

Use it as a library:

```python
import bitranox_template_py_lib as lib

lib.emit_greeting()      # writes "Hello World" to stdout
lib.print_info()         # print the package metadata block
```

See [docs/usage.md](docs/usage.md) for the full command and API reference.

## Documentation

- [Installation](docs/installation.md)
- [Usage](docs/usage.md)
- [Development](docs/development.md)
- [Module Reference](docs/systemdesign/module_reference.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
- [Our stance on AI](ai-stance.md)
- [AI transparency](ai-transparency.md)
- [License](LICENSE)
