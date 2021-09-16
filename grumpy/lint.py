import pathlib
from .reporter import Reporter, console
from .utils import create_register
import subprocess


LINT_CHECKS = dict()
register = create_register(LINT_CHECKS)


def unregister(name: str) -> None:
    LINT_CHECKS.pop(name)
    return None


@register
@Reporter
def has_flake8() -> bool:
    """
    Checks for the existence of a flake 8 file
    """
    retval = True, "OK"
    if not pathlib.Path(".flake8").exists():
        retval = False, "Missing .flake8"
    return retval


@register
@Reporter
def run_flake8() -> bool:
    retval = True, "OK"
    output = subprocess.run(
        'flake8', capture_output=True
    )
    if output.returncode != 0:
        retval = False, '\n'.join([output.stdout.decode('utf8'), output.stderr.decode('utf8')])
        console.print(output.stdout.decode('utf8'))
        console.print(output.stderr.decode('utf8'))
    return retval
