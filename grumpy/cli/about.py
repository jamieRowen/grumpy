from cleo import Command
from ..commands import ALL_CHECKS
from ..commands import FINAL_MESSAGE
from .cat import cat, random_phrase
from ..reporter import console


class AboutCommand(Command):
    """
    Grumpily runs a check

    about
        {command : What are you grumpy about?}
    """

    def handle(self):
        command = 'check_' + self.argument('command')
        ALL_CHECKS[command]()
        if FINAL_MESSAGE['issues'] == 0:
            console.print(
                cat, style="black on white"
            )
            console.print(
                "Great work, I hate it."
            )
        else:
            console.print(random_phrase())
