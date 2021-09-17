from cleo import Command
from rich.table import Table
from ..commands import ALL_CHECKS
from ..commands import FINAL_MESSAGE
from .cat import cat, random_phrase
from ..reporter import console


class AboutCommand(Command):
    """
    Grumpily runs a check

    about
        {command : What are you grumpy about?}
        {--topic=? : For asking about a specific topic}
    """
    

    def handle(self):
        if self.argument('command') == "what":
            return self._handle_what()
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
    
    def _handle_what(self):
        what_option = self.option('topic')
        
        available_commands = [s.replace("check_", "") for s in ALL_CHECKS.keys()]
        table = Table(show_header=True)
        table.add_column("Command")
        table.add_column("Description")
        for com in available_commands: 
            table.add_row(com, "")
        console.print(table)
