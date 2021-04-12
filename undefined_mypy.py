from typing import Any, Callable, Optional

from mypy.plugin import AnalyzeTypeContext, Plugin
from mypy.types import Type, UnionType


class CustomPlugin(Plugin):
    def get_type_analyze_hook(self, fullname: str) -> Optional[Callable[[AnalyzeTypeContext], Type]]:
        if fullname == "undefined.Undefined":
            return undefined_type_hook

        return None


def undefined_type_hook(ctx: AnalyzeTypeContext) -> Type:
    undefined_type = ctx.api.named_type("undefined.Undefined", [])

    if not ctx.type.args:
        return ctx.api.analyze_type(undefined_type)

    return ctx.api.analyze_type(UnionType([undefined_type, *ctx.type.args]))


def plugin(version: str) -> Any:
    return CustomPlugin


__all__ = ["plugin"]
