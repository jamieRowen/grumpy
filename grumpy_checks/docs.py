import subprocess
from typing import Iterator, Tuple
from .checks import (
    CheckCollection, CheckResponse,
    as_CheckResponse, call_check_collection
)


DOCS_CHECKS = CheckCollection("docs")


def check_docs() -> Iterator[CheckResponse]:
    return call_check_collection(DOCS_CHECKS)


@DOCS_CHECKS.register
@as_CheckResponse
def run_pydocstyle() -> Tuple[bool, str]:
    retval = True, ""
    output = subprocess.run(
        'pydocstyle', capture_output=True
    )
    if output.returncode:
        retval = False, '\n'.join(
            [output.stdout.decode("utf8"), output.stderr.decode("utf8")]
        )
    return retval
