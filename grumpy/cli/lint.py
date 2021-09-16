from cleo import Command
from ..commands import check_lint

class LintCommand(Command):
    """
    Runs lint checks

    lint
    """

    def handle(self):
        check_lint()
