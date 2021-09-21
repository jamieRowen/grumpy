from .utils import detect_package_details, has_pyproject_toml
from .checks import CheckResponse, CheckCollection
from .checks import as_CheckResponse, call_check_collection
from typing import Iterator, Tuple
from datetime import date
import re
import pathlib


NEWS_CHECKS = CheckCollection("news")


def check_news() -> Iterator[CheckResponse]:
    """Run all registered lnews checks

    This is really just a wrapper for NEWS_CHECKS()
    callable object, that adds a table summary of output
    from the resultant generator
    """
    return call_check_collection(NEWS_CHECKS)


@NEWS_CHECKS.register
@as_CheckResponse
def has_newsfile() -> Tuple[bool, str]:
    """Check for presence of NEWS.md
    """
    retval = True, ""
    if not pathlib.Path("NEWS.md").exists():
        retval = False, "Missing NEWS.md"
    return retval


@NEWS_CHECKS.register
@as_CheckResponse
def newsfile_format() -> Tuple[bool, str]:
    """Check that the NEWS.md has the appropriate format
    """
    has_files, retval = _has_necessary_files()
    if not has_files:
        return retval
    message = ""
    failflag = False
    pkg_details = detect_package_details()
    news = _read_news()[:3]
    expected_first_line = fr"## {pkg_details['name']} {pkg_details['version']} [_\*]20\d{{2}}-\d{{2}}-\d{{2}}[_\*]$"  # noqa: E501 ignore line length lint in this case
    expected_second_line = r"^\s+$"
    expected_third_line = r"^\s+\* "
    if re.match(expected_first_line, news[0].strip()) is None:
        failflag = True
        message += f"""
        NEWS.md L1:
        Expected [green]{expected_first_line[:-30] + str(date.today())}[/green]
        Found [red]{news[0]}[/red]

        """
    if re.match(expected_second_line, news[1]) is None:
        failflag = True
        message += f"""
        NEWS.md L2:
        Expected [green]blank line[/green]
        Found [red]{news[1]}[/red]

        """
    if re.match(expected_third_line, news[2]) is None:
        failflag = True
        message += f"""
        NEWS.md L3:
        Expected [green]    * [/green]
        Found [red]{news[2]}[/red]

        """
    retval = True, "Ok"
    if failflag:
        retval = False, message
    return retval


def _has_necessary_files() -> Tuple[bool, Tuple[bool, str]]:
    has_news = has_newsfile()
    has_toml = has_pyproject_toml()
    if not has_toml and not has_news.result:
        return False, (False, "Missing [NEWS.md, pyproject.toml]")
    elif not has_news.result:
        return False, (has_news.result, has_news.info)
    elif not has_toml:
        return False, (False, "Missing pyproject.toml")
    else:
        return True, (True, "")


@NEWS_CHECKS.register
@as_CheckResponse
def news_version_matches_toml() -> Tuple[bool, str]:
    has_files, retval = _has_necessary_files()
    if not has_files:
        return retval
    pkg_details = detect_package_details()
    news = _read_news()[0]
    rex = r"\d+.\d+.\d+"
    res = re.search(rex, news)
    news_version = news[res.start():res.end()]
    toml_version = pkg_details['version']
    toml_colour, news_colour = "red", "green"
    if toml_version > news_version:
        toml_colour, news_colour = "green", "red"

    retval = True, "OK"
    if news_version != toml_version:
        message = f"""
        NEWS.md Version mismatch:
        [{toml_colour}]Pyproject.toml gives {toml_version}[/{toml_colour}]
        [{news_colour}]NEWS.md gives {news_version}[/{news_colour}]

        """
        retval = False, message
    return retval


def _read_news() -> str:
    if has_newsfile():
        return _get_news()
    else:
        return ""


def _get_news() -> str:
    with open("NEWS.md") as f:
        res = f.readlines()
    return res
