import sys

import click
from blessings import Terminal

from ward.collect import get_info_for_modules, get_tests_in_modules, load_modules
from ward.fixtures import fixture_registry
from ward.suite import Suite
from ward.terminal import SimpleTestResultWrite, ExitCode
from ward.test_result import TestOutcome


@click.command()
@click.option(
    "-p", "--path", default=".", type=click.Path(exists=True), help="Path to tests."
)
@click.option(
    "-f", "--filter", help="Only run tests whose names contain the filter argument as a substring."
)
def run(path, filter):
    term = Terminal()

    mod_infos = get_info_for_modules(path)
    modules = list(load_modules(mod_infos))
    tests = list(get_tests_in_modules(modules, filter=filter))

    suite = Suite(tests=tests, fixture_registry=fixture_registry)

    test_results = suite.generate_test_runs()

    results = SimpleTestResultWrite(terminal=term, suite=suite).output_all_test_results(test_results)
    if any(r.outcome == TestOutcome.FAIL for r in results):
        exit_code = ExitCode.TEST_FAILED
    else:
        exit_code = ExitCode.SUCCESS

    sys.exit(exit_code.value)
