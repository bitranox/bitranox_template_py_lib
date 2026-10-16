# Usage

This is a template, so the shipped CLI and API are deliberately small: enough to prove that
packaging, entry points, error handling and doctests all work end to end, and nothing more.
Replace the placeholder behaviors with your own once you clone it.

## Command-line interface

The CLI is built on [rich-click](https://github.com/ewels/rich-click), so help, errors and
tracebacks render with Rich styling while keeping click's ergonomics. Both console commands
(`bitranox_template_py_lib` and `bitranox-template-py-lib`) and `python -m
bitranox_template_py_lib` invoke the same entry point.

### Commands

| Command | What it does                                                            |
|---------|-------------------------------------------------------------------------|
| `info`  | Print resolved package metadata (name, version, homepage, author, ...). |
| `hello` | Emit the canonical greeting `Hello World`.                              |
| `fail`  | Raise an intentional `RuntimeError` to exercise error handling.         |

### Global options

| Option                         | Effect                                                                                 |
|--------------------------------|----------------------------------------------------------------------------------------|
| `--traceback / --no-traceback` | Show a full Rich traceback on error, or a single-line message. Default: `--traceback`. |
| `--version`                    | Print the version and exit.                                                            |
| `-h`, `--help`                 | Show help and exit.                                                                    |

### Examples

```bash
bitranox_template_py_lib hello                 # -> Hello World
bitranox_template_py_lib info                  # metadata block
bitranox_template_py_lib fail                  # full traceback on stderr, exit code 1
bitranox_template_py_lib --no-traceback fail   # one-line error on stderr, exit code 1
bitranox_template_py_lib --version

# same behavior, other entry points:
bitranox-template-py-lib info
python -m bitranox_template_py_lib info
uvx bitranox_template_py_lib info
```

### Exit codes

`main()` hands the command group to `lib_cli_exit_tools.run_cli()`, which maps the outcome:

| Outcome                        | Exit code                                         |
|--------------------------------|---------------------------------------------------|
| Command completes              | `0`                                               |
| Command calls `ctx.exit(n)`    | `n` - use this to report "ran fine, answer is no" |
| `SystemExit(n)`                | `n`                                               |
| Ctrl-C (`KeyboardInterrupt`)   | `130`, after printing `Aborted (SIGINT).`         |
| A `ClickException` (bad usage) | Click's own code, after it shows the message      |
| Any other uncaught exception   | Errno-derived, `1` when nothing more specific     |

Diagnostics go to stderr, so `bitranox_template_py_lib hello > out.txt` keeps errors on the
terminal and only the command's data in the file.

## Library API

The public surface is re-exported from the package root:

```python
import bitranox_template_py_lib as lib

# success path: write the canonical greeting to a stream (default: stdout)
lib.emit_greeting()

# to any object with a write() method:
from io import StringIO

buffer = StringIO()
lib.emit_greeting(stream=buffer)
assert buffer.getvalue() == "Hello World\n"

# deterministic failure, for exercising error handling:
try:
    lib.raise_intentional_failure()
except RuntimeError as exc:
    print(f"caught expected failure: {exc}")  # I should fail

# print the package metadata block:
lib.print_info()
```

### Exported names

| Name                        | Kind     | Purpose                                                 |
|-----------------------------|----------|---------------------------------------------------------|
| `CANONICAL_GREETING`        | constant | The greeting text (`"Hello World"`).                    |
| `WritableStream`            | Protocol | Structural type for any object with `write(str)`.       |
| `emit_greeting`             | function | Write the greeting to a stream (keyword-only `stream`). |
| `raise_intentional_failure` | function | Always raise `RuntimeError("I should fail")`.           |
| `noop_main`                 | function | Placeholder callable that does nothing.                 |
| `print_info`                | function | Print the metadata block used by the `info` command.    |

For a module-by-module breakdown with source anchors, see
[systemdesign/module_reference.md](systemdesign/module_reference.md).
