"""CLI stories: every invocation a single beat."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
import rich_click as click

from bitranox_template_py_lib import __init__conf__
from bitranox_template_py_lib import cli as cli_mod

if TYPE_CHECKING:
    from click.testing import CliRunner, Result


@pytest.mark.os_agnostic
def test_when_cli_runs_without_arguments_help_is_printed(
    monkeypatch: pytest.MonkeyPatch,
    cli_runner: CliRunner,
) -> None:
    """When CLI runs without arguments, help should be displayed."""
    calls: list[str] = []

    def remember() -> None:
        calls.append("called")

    monkeypatch.setattr(cli_mod, "noop_main", remember)

    result = cli_runner.invoke(cli_mod.cli, [])

    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert calls == []


@pytest.mark.os_agnostic
def test_when_traceback_is_requested_without_command_the_domain_runs(
    monkeypatch: pytest.MonkeyPatch,
    cli_runner: CliRunner,
) -> None:
    """When --traceback is provided without command, noop_main should run."""
    calls: list[str] = []

    def remember() -> None:
        calls.append("called")

    monkeypatch.setattr(cli_mod, "noop_main", remember)

    result = cli_runner.invoke(cli_mod.cli, ["--traceback"])

    assert result.exit_code == 0
    assert calls == ["called"]
    assert "Usage:" not in result.output


@pytest.mark.os_agnostic
def test_default_shows_traceback(capsys: pytest.CaptureFixture[str]) -> None:
    """By default (no flags), full traceback should appear on errors."""
    exit_code = cli_mod.main(["fail"])

    assert exit_code != 0

    captured = capsys.readouterr()
    output = captured.out + captured.err
    assert "Traceback" in output


@pytest.mark.os_agnostic
def test_no_traceback_flag_suppresses_traceback(capsys: pytest.CaptureFixture[str]) -> None:
    """When --no-traceback is used, only simple error message should appear."""
    exit_code = cli_mod.main(["--no-traceback", "fail"])

    assert exit_code != 0

    captured = capsys.readouterr()
    output = captured.out + captured.err
    assert "RuntimeError: I should fail" in output
    assert "Traceback" not in output


@pytest.mark.os_agnostic
def test_when_hello_is_invoked_the_cli_smiles(cli_runner: CliRunner) -> None:
    """Hello command should output the canonical greeting."""
    result: Result = cli_runner.invoke(cli_mod.cli, ["hello"])

    assert result.exit_code == 0
    assert result.output == "Hello World\n"


@pytest.mark.os_agnostic
def test_when_fail_is_invoked_the_cli_raises(cli_runner: CliRunner) -> None:
    """Fail command should raise RuntimeError."""
    result: Result = cli_runner.invoke(cli_mod.cli, ["fail"])

    assert result.exit_code != 0
    assert isinstance(result.exception, RuntimeError)


@pytest.mark.os_agnostic
def test_when_info_is_invoked_the_metadata_is_displayed(cli_runner: CliRunner) -> None:
    """Info command should display package metadata."""
    result: Result = cli_runner.invoke(cli_mod.cli, ["info"])

    assert result.exit_code == 0
    assert f"Info for {__init__conf__.name}:" in result.output
    assert __init__conf__.version in result.output


@pytest.mark.os_agnostic
def test_when_an_unknown_command_is_used_a_helpful_error_appears(cli_runner: CliRunner) -> None:
    """Unknown commands should produce a helpful error message."""
    result: Result = cli_runner.invoke(cli_mod.cli, ["does-not-exist"])

    assert result.exit_code != 0
    assert "No such command" in result.output


@pytest.mark.os_agnostic
def test_main_returns_zero_on_success() -> None:
    """Main should return 0 for successful commands."""
    exit_code = cli_mod.main(["hello"])
    assert exit_code == 0


@pytest.mark.os_agnostic
def test_main_returns_nonzero_on_failure() -> None:
    """Main should return non-zero for failed commands."""
    exit_code = cli_mod.main(["fail"])
    assert exit_code != 0


@pytest.mark.os_agnostic
def test_version_option_displays_version(cli_runner: CliRunner) -> None:
    """--version should display the package version."""
    result = cli_runner.invoke(cli_mod.cli, ["--version"])

    assert result.exit_code == 0
    assert __init__conf__.version in result.output
    assert __init__conf__.shell_command in result.output


@pytest.mark.os_agnostic
def test_main_translates_system_exit_into_its_exit_code(monkeypatch: pytest.MonkeyPatch) -> None:
    """A SystemExit escaping a command should surface as that exit code."""

    @click.command("boom")
    def boom() -> None:
        raise SystemExit(42)

    monkeypatch.setattr(cli_mod, "cli", boom)

    assert cli_mod.main([]) == 42


@pytest.mark.os_agnostic
def test_main_reports_the_code_a_command_passed_to_ctx_exit(monkeypatch: pytest.MonkeyPatch) -> None:
    """A command that ends normally still reports its own ``ctx.exit()`` code.

    Click runs with ``standalone_mode=False``, so ``ctx.exit(n)`` is *returned*
    rather than raised. Dropping that value would collapse "ran fine, the
    answer is no" into success, which is what lib_cli_exit_tools 2.3.4 fixed.
    """

    @click.command("nothing-found")
    @click.pass_context
    def nothing_found(ctx: click.Context) -> None:
        ctx.exit(3)

    monkeypatch.setattr(cli_mod, "cli", nothing_found)

    assert cli_mod.main([]) == 3


@pytest.mark.os_agnostic
def test_help_option_displays_help(cli_runner: CliRunner) -> None:
    """--help should display usage information."""
    result = cli_runner.invoke(cli_mod.cli, ["--help"])

    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "--traceback" in result.output
