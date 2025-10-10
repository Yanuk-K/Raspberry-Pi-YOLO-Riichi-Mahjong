from Mahjong_rules.Yaku.utils import HandContext, Yaku


class RinshanKaihou(Yaku):
    def __init__(self) -> None:
        super().__init__("Rinshan Kaihou", 1, 1)

    def hasYaku(self, ctx: HandContext) -> bool:
        return ctx.is_rinshan


__all__ = ["RinshanKaihou"]
