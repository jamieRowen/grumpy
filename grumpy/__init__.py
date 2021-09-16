from .reporter import console
from .lint import LINT_CHECKS
from .utils import create_register


ALL_CHECKS = dict()
FINAL_MESSAGE = {
    'lint': 0
}
register = create_register(ALL_CHECKS)


@register
def check_lint():
    """
    Run all registered lint checks, see dir(grumpy.lint)
    for specific check functions
    """
    results = dict()
    strings = dict()
    for k, v in LINT_CHECKS.items():
        res, string = v()
        strings[k] = string
        results[k] = res
    
    if not all([res for _, res in results.items()]):
        console.print(" \
            [red] Issues with lint checks [/red]\n \
            See grumpy_feedback/lints.txt for saved info \
        ")
