import datetime
from grumpy.lint import unregister
from .reporter import console, Reporter
from .utils import create_register, create_unregister, detect_package_details
from typing import Tuple
from datetime import date
import re
import pathlib

NEWS_CHECKS = dict()

register = create_register(NEWS_CHECKS)
unregister = create_unregister(NEWS_CHECKS)

@register
@Reporter
def has_newsfile() -> Tuple[bool, str]:
    """Check for presence of News.md
    """
    retval = True, "OK"
    if not pathlib.Path("NEWS.md").exists():
        retval = False, "Missing NEWS.md"
    return retval


@register
@Reporter
def newsfile_format() -> Tuple[bool, str]:
    """
    """
    message = ""
    failflag = False
    pkg_details = detect_package_details()
    news = _read_news()[:3]
    expected_first_line = fr"## {pkg_details['name']} {pkg_details['version']} [_\*]20\d{{2}}-\d{{2}}-\d{{2}}[_\*]$"
    expected_second_line =  fr"^\s+$"
    expected_third_line = fr"^\s+\* "
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
        console.print(message)
    return retval


@register
@Reporter
def news_version_matches_toml():
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
        console.print(message)
    return retval


def _read_news() -> str:
    with open("NEWS.md") as f:
        res = f.readlines()
    return res
