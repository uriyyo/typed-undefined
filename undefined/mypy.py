from typing import Any, Callable, Optional

from mypy.plugin import AnalyzeTypeContext, Plugin
from mypy.types import Type, UnionType


class CustomPlugin(Plugin):
    def get_type_analyze_hook(self, fullname: str) -> Optional[Callable[[AnalyzeTypeContext], Type]]:
        if fullname == "undefined.Undefined":
            return undefined_type_hook

        return None


def undefined_type_hook(ctx: AnalyzeTypeContext) -> Type:
    args = [ctx.api.named_type("undefined.Undefined", []), *ctx.type.args]
    return ctx.api.analyze_type(UnionType.make_union(args))


def plugin(version: str) -> Any:
    return CustomPlugin


__all__ = ["plugin"]
