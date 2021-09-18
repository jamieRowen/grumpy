from dataclasses import dataclass
import functools
from typing import Callable, Any, Iterator
from types import GeneratorType
from rich import console
from rich.live import Live
from rich.repr import Result
from rich.table import Table
from rich.console import Console

console = Console()

@dataclass
class CheckResponse:
    name: str
    result: bool
    info: str


@dataclass
class CollectionResponse:
    group: str
    result: CheckResponse


class CheckCollectionGroup:
    def __init__(self):
        self.collection = dict()
        self.issues = 0
    
    def register(self, collection: CheckCollection):
        self.collection[collection.name] = collection
        @functools.wraps(collection)
        def inner_register():
            return collection()
        return inner_register
    
    def __call__(self):
        CORRECT = "[green]:heavy_check_mark:[/green]"
        INCORRECT = "[red]:heavy_check_mark:[/red]"
        table = Table()
        table.add_column("Group")
        table.add_column("Check")
        table.add_column("Result")
        with Live(table, refresh_per_second=30):
            for _, collection in self.collection.items():
                for _, func in collection.collection.items():
                    res = func()
                    table.add_row(collection.name, res.name, (res.result and CORRECT) or INCORRECT)
        console.print()
        


class CheckCollection:
    def __init__(self, name: str, logging: bool=True) -> None:
        self.name = name
        self.__name__ = name
        self.collection = dict()
        self.logging = logging
        self.issues = 0
        self.message = ""
    
    def register(self, func: Callable[[Any], CheckResponse]) -> Callable[[Any], CheckResponse]:
        self.collection[func.__name__] = func
        @functools.wraps(func)
        def inner_register():
            return func()
        return inner_register
    
    def __call__(self) -> Iterator[CollectionResponse]:
        issues = 0
        message = ""
        for k, v in self.collection.items():
            res = v()
            yield CollectionResponse(self.name, res)
#             if not res.result:
#                 issues += 1
#                 message += f"""
# {res.name}

# {res.info}
#                 """
#         self.issues += issues
#         self.message += message
        



class RunnableChecks:
    def __init__(self, checks: dict, fstub: str, name: str = None) -> None:
        self.fstub = fstub
        self.checks = checks
        self.results = dict()
        self.strings = dict()
        self.issues = 0
        self.name = name or fstub
    
    def __call__(self, *args, **kwargs):
        for k, v in self.checks.items():
            res, string = v()
            self.issues += not res
            self.strings[k] = string
            self.results[k] = res
            yield self.name, k, res, string, self.fstub