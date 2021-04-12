from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

from typing_extensions import final

T = TypeVar("T")


class _UndefinedMeta(type):
    __instance__: Optional[_Undefined] = None

    def __new__(
        mcs,
        name: str,
        bases: Tuple[Type, ...],
        namespace: Dict[str, Any],
    ) -> Any:
        try:
            _ = _Undefined  # check if undefined is defined
        except NameError:
            return super().__new__(mcs, name, bases, namespace)

        raise RuntimeError("Can't subclass Undefined")

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if args or kwargs:
            raise TypeError("Undefined does not accept args and kwargs")

        if cls.__instance__ is None:
            cls.__instance__ = super().__call__()

        return cls.__instance__


@final
class _Undefined(metaclass=_UndefinedMeta):
    __name__ = "Undefined"
    __qualname__ = "Undefined"

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "Undefined()"

    def __str__(self) -> str:
        return "undefined"

    def __class_getitem__(cls, item: T) -> Undefined[T]:
        return cast(Union[_Undefined, T], Union[cls, item])


undefined = _Undefined()

if TYPE_CHECKING:  # pragma: no cover
    Undefined = Union[_Undefined, T]
else:
    Undefined = _Undefined


def resolve(val: Undefined[T], default: T) -> T:
    return cast(T, val if val is not undefined else default)


__all__ = [
    "resolve",
    "undefined",
    "Undefined",
]
