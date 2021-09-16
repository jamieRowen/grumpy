from cleo import Command, Application
from .cli.lint import LintCommand

application = Application()
application.add(LintCommand())

def main():
    application.run()

if __name__ == '__main__':
    main()
