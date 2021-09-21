"""Scripts for easier development.

Shortcut scripts for poetry for
running standard routines like
test, code coverage and documentation.
"""

import subprocess


def test():
    """Run tests.

    Run all unittests. Equivalent to:
    `poetry run python -u -m unittest discover -s tests -v -p "*.py"`
    """
    subprocess.run(
        [
            'python', '-u', '-m', 'unittest',
            'discover', '-s', 'tests', '-v', '-p',
            '*.py'
        ]
    )


def _coverage():
    """Coverage.

    Run a coverage report. Equivalent to:
    `poetry run coverage run -m unittest discover -s tests -p '*.py'`
    """
    subprocess.run(
        [
            'python', '-m',
            'coverage', 'run', '-m', 'unittest',
            'discover', '-s', 'tests', '-p', '*.py'
        ]
    )


def coverage_report():
    """Coverage report.

    Report on coverage report
    Equivalent to:
    ```
    poetry run coverage run -m unittest discover -s tests -p '*.py'
    poetry run coverage report
    ```
    """
    _coverage()
    subprocess.run(
        ['python', '-m', 'coverage', 'report']
    )


def documentation():
    """Documentation.

    Create documentation from docstrings as set of html pages
    Equivalent to:
    `poetry run pydoctor --make-html --html-output=docs/api grumpy_checks`
    """
    subprocess.run(
        [
            'python', '-m', 'pydoctor',
            '--make-html', '--html-output=docs/api',
            'grumpy_checks'
        ]
    )
