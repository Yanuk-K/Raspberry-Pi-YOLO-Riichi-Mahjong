from Mahjong_rules.Yaku.utils import HandContext, Yaku


class Riichi(Yaku):
    def __init__(self) -> None:
        super().__init__("Riichi", 1, 0)

    def hasYaku(self, ctx: HandContext) -> bool:
        return ctx.riichi


__all__ = ["Riichi"]
