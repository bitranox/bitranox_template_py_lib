# Installation

`bitranox_template_py_lib` is a normal PEP 621 package. Every method below registers two
console commands on your PATH: `bitranox_template_py_lib` and `bitranox-template-py-lib`
(both point at the same CLI).

The examples use [uv](https://docs.astral.sh/uv/), a fast Rust-based replacement for
`pip`, `venv`, `pipx` and `poetry`. Nothing here requires uv; the plain `pip` equivalents
follow.

## Requirements

- Python 3.10 or newer.
- Runtime dependencies (installed automatically): `rich-click` for the CLI,
  `lib_cli_exit_tools>=2.3.4` for signal handling and exit codes, and `rtoml>=0.13`
  for TOML parsing.

## Install uv (optional)

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# or, with an existing Python
python -m pip install uv
```

## 1. Into a virtual environment (uv)

```bash
uv venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
uv pip install bitranox_template_py_lib
# from GitHub instead of PyPI:
uv pip install "git+https://github.com/bitranox/bitranox_template_py_lib"
```

## 2. As a persistent CLI tool (uv)

Installs into an isolated environment and puts the commands on your PATH:

```bash
uv tool install bitranox_template_py_lib
uv tool upgrade bitranox_template_py_lib
# from GitHub:
uv tool install --from "git+https://github.com/bitranox/bitranox_template_py_lib.git" bitranox-template-py-lib
```

## 3. Run once, without installing (uvx)

```bash
uvx bitranox_template_py_lib info
uvx --from "git+https://github.com/bitranox/bitranox_template_py_lib.git" bitranox_template_py_lib info
```

## 4. Plain pip

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install bitranox_template_py_lib
# from GitHub:
pip install "git+https://github.com/bitranox/bitranox_template_py_lib"
# editable, with dev tooling, for working on the package itself:
pip install -e ".[dev]"
```

## 5. Per-user install (no virtualenv)

```bash
pip install --user bitranox_template_py_lib
```

This respects PEP 668, so it is refused on an externally-managed system Python. Make sure
`~/.local/bin` is on your PATH so the commands are found.

## 6. pipx

```bash
pipx install bitranox_template_py_lib
pipx upgrade bitranox_template_py_lib
```

## 7. From build artifacts

```bash
python -m build
pip install dist/bitranox_template_py_lib-*.whl
```

## Why we recommend uv: supply-chain protection

This repository commits a `uv.lock`. It pins every package the project needs, transitive
dependencies included, to an exact version and to the hashes of that version's files. The
`exclude-newer` setting under `[tool.uv]` in `pyproject.toml` adds a cooldown: uv leaves any
release younger than that out of the lock. CI installs from the lock, so a hijacked release that
gets pulled again within the cooldown never reaches our builds, and a file whose hash does not
match is refused.

That protection stays in this repository. The installable package declares only lower bounds
(`>=`) for its dependencies, so a plain `pip install` takes the newest release of every transitive
dependency at the moment you run it. If one of them was hijacked an hour earlier, you get the
hijacked version. `pipx install` and `uv tool install` without options do the same.

To install the command line tool with a cooldown of your own (uv then skips any release younger
than 7 days, transitive ones included), or to run the exact tree our CI tests:

```bash
uv tool install --exclude-newer "7 days" bitranox_template_py_lib
git clone https://github.com/bitranox/bitranox_template_py_lib.git && cd bitranox_template_py_lib && uv sync --locked && uv run bitranox_template_py_lib --help
```

If you depend on bitranox_template_py_lib in your own project, give that project the same cooldown (7 days here, as
an example) and commit the `uv.lock` that `uv add bitranox_template_py_lib` writes:

```toml
[tool.uv]
exclude-newer = "7 days"
```

