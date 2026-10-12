# Changelog

All notable changes to this project will be documented in this file following
the [Keep a Changelog](https://keepachangelog.com/) format.

## [Unreleased]

## [2.0.2] 2026-10-12 22:51:08

### Added

- Python 3.15 is declared and tested: the classifier puts it into the CI matrix and
  `make test-all`, and `make test` now builds the development venv on 3.15.
- `uv.lock` is committed, and `[tool.uv] exclude-newer` sets a cooldown that keeps releases younger
  than it out of the lock. CI installs exactly the locked tree on push and pull request; the nightly
  scheduled run still resolves afresh to catch upstream breakage early.

### Changed

- The devcontainer image and interpreter path move from Python 3.13 to 3.14.
- Requires `rtoml>=0.14.0` (and, in the dev extra, `ruff>=0.17.0`, `pydantic>=2.14.1`); the
  Makefile is bmk 3.19.0.
- The install section explains why installing with uv protects against supply-chain attacks and why
  a plain `pip install` from PyPI does not.

## [2.0.1] 2026-07-30 18:06:55

### Changed

- **The shipped skill's plugin version now tracks the package version.** bmk 3.14.0 raises
  `.claude-plugin/plugin.json` to the package version on bump, push and release, and never lowers
  it. An install re-fetches a skill only when that version changes, so the two numbers drifting
  apart meant a skill edit could ship to nobody. No functional change to the library.

## [2.0.0] 2026-07-29

### Removed
- **BREAKING:** Python 3.9 support. `requires-python` is now `>=3.10`, matching the floor of the
  bitranox runtime libraries this template builds on. Installs on 3.9 will no longer resolve.
- Every `python_version<'3.10'` / `python_version>='3.10'` environment marker in the runtime
  dependencies, the `dev` extra, and `build-system.requires`, along with the caps they carried
  (`rtoml<0.13`, `pytest<9`, `bandit<1.9`, `build<1.5.0`, `pip-audit<2.10`, `import-linter<2.6`,
  `setuptools<83`, `hatchling<1.28`). Each list is now a single unconditional floor. The `click`
  CVE pin loses its marker for the same reason.
- `cli._exit_code_from` and `cli._print_error`, plus the module-level `console` and the rich
  traceback installation they depended on. `lib_cli_exit_tools` covers all of it.
- All nine `[tool.pip-audit].ignore-vulns` entries. Audited with zero ignore flags, from outside
  the project so no config could apply: both the 75-package resolved dev tree and the project
  `.venv` report no known vulnerabilities. Every id was inert, either because the package left
  the tree (`py`, Pillow) or because it resolved past the fix (pip 26.1.2, cryptography 49.0.0,
  requests 2.34.2, filelock 3.32.0 against fixes in 3.20.1 / 3.20.3). The table stays, empty,
  with the policy for adding an id written next to it. The old comment was also wrong on the
  facts: it described `GHSA-4xh5-x5gv-qwph` as a `py` ReDoS aliased to `PYSEC-2022-42969`, but
  it is a pip symlink advisory and the two are not aliases.

### Added
- `lib_cli_exit_tools>=2.3.4` as a runtime dependency. `main()` now publishes the traceback
  preference to `lib_cli_exit_tools.config` and runs the command group through
  `run_cli()`, which brings signal handling the template previously lacked: Ctrl-C exits 130
  with a clean `Aborted (SIGINT).` message instead of dumping a `KeyboardInterrupt` traceback,
  and SIGTERM/SIGBREAK are handled the same way.
- A regression test pinning that a command's `ctx.exit(n)` code survives to the process exit
  status, and one pinning `SystemExit` translation.
- The `integration` pytest marker, which this project had never declared even though
  `make testintegration` targets it. A project scaffolded from this template now inherits the
  marker, so its first `@pytest.mark.integration` test does not fire an unknown-marker warning.
  The template itself still has no integration tests, so the target collects nothing.

### Fixed
- `main()` returned a hardcoded `0` on the non-exception path, discarding whatever the command
  passed to `ctx.exit()`. Click runs with `standalone_mode=False`, which makes it *return* that
  code rather than raise it, so a command reporting a negative answer - nothing found, host did
  not respond - exited `0` and read as success. This is the same defect fixed upstream in
  `lib_cli_exit_tools` 2.3.4, and adopting the library fixes it here.
- `main()` treated an explicitly empty `argv=[]` as "no argv given" and fell back to
  `sys.argv[1:]` when sniffing for `--no-traceback`, while passing the empty list on to Click.
  The check is now `argv is not None`, so both paths see the same arguments.
- Error output goes to stderr instead of stdout, so a shell pipeline no longer mixes
  diagnostics into the command's data.

### Changed
- `ruff`'s `target-version` is `py310`.
- `CliContext` is declared with `slots=True`, so assigning an undeclared attribute raises
  instead of silently attaching it to the shared context object.
- `typed_click._CommandDecorator` is annotated `TypeAlias` (PEP 613) and the module now carries
  `from __future__ import annotations` like the rest of the package.
- The one-line error summary is now `RuntimeError: ...` rather than `Error: RuntimeError: ...`;
  the `Error: ` prefix was local to the removed `_print_error`.

## [1.1.3] 2026-07-24 15:56:45

### Changed
- Pinned the lint policy explicitly: added the curated `[tool.ruff.lint].select` list (the same
  family set as `bitranox_template_py_cli`) plus matching `tests/*.py` per-file-ignores, so a future
  ruff release widening its default rule set no longer reddens CI with hundreds of unrelated
  findings.
- Made the root `cli` group callback's `traceback` parameter keyword-only (`PLR0917`); Click still
  invokes it via `**ctx.params`, so no call site changed.

### Fixed
- Replaced `print()` with `sys.stdout.write()` in `__init__conf__.print_info()` (`T201`), matching the
  established fix in `bitranox_template_py_cli`.
- Sorted `__all__` in `behaviors.py` (`RUF022`) and normalized import ordering across `src` and
  `tests` (`I001`, `TC002`, `TC003`).

## [1.1.2] 2026-06-14

### Changed
- Added a `typed_click.py` facade wrapping rich-click's `option` / `version_option` decorators behind explicit, fully-known signatures, keeping the CLI strict-clean under pyright (`reportUnknownMemberType`) without disabling the rule (ignore isolated to the facade).

## [1.1.1] - 2026-02-18

### Added
- `__all__` export declaration in `__init__conf__.py` for consistent public API surface

### Fixed
- Pin `rtoml` and `pip-audit` versions for Python 3.9 compatibility
- Ignore `filelock` transitive dependency vulnerabilities in pip-audit

## [1.1.0] - 2026-02-18

### Added
- `WritableStream` Protocol for narrower stream typing in `behaviors.py`
- `CliContext` dataclass replacing untyped dict for Click context storage
- Dynamic CI matrix extracting Python versions from pyproject.toml classifiers
- Pydantic models for typed TOML parsing in test suite
- Test covering `SystemExit` branch in `cli.main()` for 100% cli.py coverage
- `pydantic` added to dev dependencies

### Changed
- Replace `TextIO` with `WritableStream` Protocol for honest, minimal typing
- Rename `ERROR_STYLE` to `_ERROR_STYLE` (private convention)
- Replace `scripts/` Python build system with bmk-based Makefile targets
- CI workflows renamed and modernized (`default_cicd_public.yml`, `default_release_public.yml`)
- Use stdlib `tomllib` instead of `rtoml` in CI setup job
- Update dev dependency pins (pydantic, ruff, pyright, bandit, etc.)

### Fixed
- CI `IndexError` in Python version parsing by switching to stdlib `tomllib`
- Inconsistent spacing in pip-audit ignore-vulns list
- Undeclared `local_only` pytest marker

### Removed
- `scripts/` directory (replaced by bmk Makefile targets)
- `CLAUDE.md` project instructions file (moved to project-level config)

## [1.0.3] - 2025-12-15

### Changed
- Move deferred imports to module top in `cli.py` for better readability
- Modernize type hints: `Optional[X]` replaced with `X | None` syntax
- Use `collections.abc.Sequence` instead of `typing.Sequence`
- Extract `_exit_code_from()` helper function with comprehensive doctests
- Extract `_print_error()` helper function for cleaner error handling
- Add `ERROR_STYLE` module-level constant for error message styling
- Add typed context documentation comment for Click context dict

### Added
- Add `__all__` export list to `cli.py` for explicit public API surface

### Fixed
- Remove unused `strip_ansi` fixture parameter from test functions
- Remove unused `Callable` import from `test_cli.py`

## [1.0.2] - 2025-12-15

### Changed
- Update CI/CD workflows to use latest GitHub Actions (cache@v5, upload-artifact@v6)
- Update dev dependencies: ruff 0.14.9, textual 6.9.0, import-linter 2.9
- Switch scripts to use rtoml for TOML parsing

### Added
- Add rtoml to dev dependencies

## [1.0.1] - 2025-12-08

### Changed
- Update dependencies to latest versions
- Update CI/CD workflows and configuration
- Convert docstrings to Google style
- Set coverage output to JSON to avoid SQL locks

## [1.0.0] - 2025-11-04
- Bootstrap `bitranox_template_py_lib`
