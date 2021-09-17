"""Check lint

This module defines and registers the various lint checking
functions. By design all checks are registered by default
and must be explicilty unregistered (grumpy.lint.unregister(name: str))
if desired to be skipped.

This module contains the following functions:

    * register - register a new function to the lint checks
    * unregister - remove a function from the collection to be checked
    * has_flake8 - ensures that a .flake8 file exists
    * run_flake8 - run the flake8 linter and capture the output

The LINT_CHECKS dictionary shows those Callables which are currently
registered in the module for checking.
"""

import pathlib
from .reporter import Reporter, console
from .utils import create_register
from typing import Tuple
import subprocess


LINT_CHECKS = dict()

register = create_register(LINT_CHECKS)


def unregister(name: str) -> None:
    """Unregister a Callable from the LINT_CHECKS

    Parameters
    ----------
    name: str
        name of a Callable that should be unregistered from the lint
        checks to be run
    """
    LINT_CHECKS.pop(name)
    return None


@register
@Reporter
def has_flake8() -> Tuple[bool, str]:
    """Checks for the existence of a flake 8 file
    """
    retval = True, "OK"
    if not pathlib.Path(".flake8").exists():
        retval = False, "Missing .flake8"
    return retval


@register
@Reporter
def run_flake8() -> Tuple[bool, str]:
    """Runs flake8 linter

    flake8 is run on a subprocess with any output captured and returned
    """
    retval = True, "OK"
    output = subprocess.run(
        'flake8', capture_output=True
    )
    if output.returncode != 0:
        retval = False, '\n'.join(
            [output.stdout.decode('utf8'), output.stderr.decode('utf8')])
        console.print(output.stdout.decode('utf8'))
        console.print(output.stderr.decode('utf8'))
    return retval
