from Mahjong_rules.Yaku.utils import HandContext, Yaku


class Chankan(Yaku):
    def __init__(self) -> None:
        super().__init__("Chankan", 1, 1)

    def hasYaku(self, ctx: HandContext) -> bool:
        return ctx.is_chankan


__all__ = ["Chankan"]
