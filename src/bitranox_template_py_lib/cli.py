"""CLI adapter wiring the behavior helpers into a rich-click interface.

Expose a stable command-line surface using rich-click for consistent,
beautiful terminal output. The CLI delegates to behavior helpers while
maintaining clean separation of concerns.

Contents:
    CLICK_CONTEXT_SETTINGS: Shared Click settings for consistent help.
    cli: Root command group with global options.
    cli_info: Print package metadata.
    cli_hello: Demonstrate success path.
    cli_fail: Demonstrate error handling.
    main: Entry point for console scripts.

Note:
    The CLI is the primary adapter for local development workflows. Packaging
    targets register the console script defined in __init__conf__. The module
    entry point (python -m) reuses the same helpers for consistency.

    Process-level concerns - signal handling, exception rendering, and the
    exception-to-exit-code mapping - are delegated to ``lib_cli_exit_tools``
    rather than reimplemented here, so every bitranox CLI exits the same way.

"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING

import lib_cli_exit_tools
import rich_click as click
from click.core import ParameterSource

from . import __init__conf__
from .behaviors import emit_greeting, noop_main, raise_intentional_failure
from .typed_click import option, version_option

if TYPE_CHECKING:
    from collections.abc import Sequence

__all__ = [
    "CLICK_CONTEXT_SETTINGS",
    "CliContext",
    "cli",
    "cli_fail",
    "cli_hello",
    "cli_info",
    "main",
]

#: Shared Click context flags for consistent help output.
CLICK_CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@dataclass(slots=True)
class CliContext:
    """Typed context object for Click's ``ctx.obj``.

    Replaces an untyped dict so that every downstream command accesses
    strongly-typed attributes instead of string-keyed dictionary items.

    Attributes:
        traceback: Whether to show full Python traceback on errors.

    """

    traceback: bool = True


@click.group(
    help=__init__conf__.title,
    context_settings=CLICK_CONTEXT_SETTINGS,
    invoke_without_command=True,
)
@version_option(
    version=__init__conf__.version,
    prog_name=__init__conf__.shell_command,
    message=f"{__init__conf__.shell_command} version {__init__conf__.version}",
)
@option(
    "--traceback/--no-traceback",
    is_flag=True,
    default=True,
    help="Show full Python traceback on errors (default: enabled)",
)
@click.pass_context
def cli(ctx: click.Context, *, traceback: bool) -> None:
    """Root command storing global flags.

    When invoked without a subcommand, displays help unless --traceback
    is explicitly provided (for backward compatibility).

    Args:
        ctx: Click context object for the command group.
        traceback: Whether to show full Python traceback on errors.

    Examples:
        >>> from click.testing import CliRunner
        >>> runner = CliRunner()
        >>> result = runner.invoke(cli, ["hello"])
        >>> result.exit_code
        0
        >>> "Hello World" in result.output
        True

    """
    # Store traceback preference in typed context object
    ctx.ensure_object(CliContext)
    ctx.obj.traceback = traceback

    # Show help if no subcommand and no explicit option
    if ctx.invoked_subcommand is None:
        source = ctx.get_parameter_source("traceback")
        if source not in (ParameterSource.DEFAULT, None):
            # Traceback was explicitly set, run default behavior
            noop_main()
        else:
            # No subcommand and default traceback value, show help
            click.echo(ctx.get_help())


@cli.command("info", context_settings=CLICK_CONTEXT_SETTINGS)
def cli_info() -> None:
    """Print resolved metadata so users can inspect installation details."""
    __init__conf__.print_info()


@cli.command("hello", context_settings=CLICK_CONTEXT_SETTINGS)
def cli_hello() -> None:
    """Demonstrate the success path by emitting the canonical greeting."""
    emit_greeting()


@cli.command("fail", context_settings=CLICK_CONTEXT_SETTINGS)
def cli_fail() -> None:
    """Trigger the intentional failure helper to test error handling."""
    raise_intentional_failure()


def main(argv: Sequence[str] | None = None) -> int:
    """Execute the CLI and return the exit code.

    This is the entry point used by console scripts and python -m execution.
    Execution runs inside a ``lib_cli_exit_tools`` session, which installs
    signal handlers, renders any escaping exception to stderr, and translates
    it into the exit code the OS expects. A command that ends normally reports
    whatever it passed to ``ctx.exit()``, so "ran fine, answer is no" stays
    distinguishable from success.

    Args:
        argv: Optional sequence of CLI arguments. None uses sys.argv.

    Returns:
        Exit code: 0 for success, non-zero for errors.

    Examples:
        >>> main(["hello"])
        Hello World
        0

    """
    argv_list = list(argv) if argv is not None else sys.argv[1:]

    # The flag is read off argv before Click parses it, because the traceback
    # preference has to be in force for failures raised during parsing too.
    show_traceback = "--no-traceback" not in argv_list

    with lib_cli_exit_tools.config_overrides(
        traceback=show_traceback,
        traceback_force_color=show_traceback,
    ):
        return lib_cli_exit_tools.run_cli(
            cli,
            argv=argv_list,
            prog_name=__init__conf__.shell_command,
        )
