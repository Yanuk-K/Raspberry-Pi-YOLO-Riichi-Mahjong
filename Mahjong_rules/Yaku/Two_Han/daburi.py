from Mahjong_rules.Yaku.utils import HandContext, Yaku


class DaburuRiichi(Yaku):
    def __init__(self) -> None:
        super().__init__("Double Riichi", 2, 0)

    def hasYaku(self, ctx: HandContext) -> bool:
        return ctx.double_riichi


__all__ = ["DaburuRiichi"]
