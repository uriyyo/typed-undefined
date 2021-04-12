# Typed Undefined

When `None` is not valid default value you can always use `undefined`.

```python
from undefined import Undefined, undefined, resolve


def foo(bar: Undefined[int] = undefined) -> int:
    return resolve(undefined, 10)


foo(1)  # ok
foo(1.0)  # error

a: Undefined[int] = 1  # ok
b: Undefined[int] = 0.5  # error
```

## mypy integration

You should add `undefined_mypy` to list of mypy plugins:

```buildoutcfg
[mypy]
plugins = undefined.mypy
```