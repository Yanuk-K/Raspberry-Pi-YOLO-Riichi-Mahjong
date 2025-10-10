from Mahjong_rules.Yaku.utils import HandContext, Yaku, is_pinfu_pattern


class Pinfu(Yaku):
    def __init__(self) -> None:
        super().__init__("Pinfu", 1, 0)

    def hasYaku(self, ctx: HandContext) -> bool:
        return any(is_pinfu_pattern(ctx, pattern) for pattern in ctx.enumerate_patterns())


__all__ = ["Pinfu"]
