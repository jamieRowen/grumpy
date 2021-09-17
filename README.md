# grumpy

`grumpy` is an opinionated set of checks for conformity of a python package. It's rule set is primarily
aimed at making sure JR folk stick to consistent guidelines.

Inspired by our grumpy co-founder Dr Gillespie

## Usage 

You can direct your grumpiness at a project by being grumpy about certain topics. For example

```
grumpy about lint
```

will execute the currently registered lint checks.

In future version you will be able to explore this information further like what lint checks are registered trough the cli 
but for now you can

```
from grumpy import lint
lint.ALL_CHECKS.keys()
```

to see the methods which are called.

If you are grumpy about everything and want all checks to be run

```
grumpy about everything
```

whereas 

```
grumpy about what
```

will show the available top level topics.

## Custom checks

It is entirely possible to add your own custom functions to be checked, each topic has a register
decorator. The runners expect a function which returns a boolean, True if passes check and a string
which gives some feedback (particularly on a failed check this is useful)

```
from grumpy.lint import register

@register
def custom_check(): -> Tuple[bool, str]
    pass
```

## Contributors

Contributions are welcome although this is still at a very early stage and the full API for grumpy is
likely to change to improve user experience.

The best example to follow for the moment is grumpy/lint.py for adding checks to a register and reporter.
New topics can be created following the lint example too.