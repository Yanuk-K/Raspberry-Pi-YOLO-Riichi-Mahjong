from Mahjong_rules.Yaku.utils import HandContext, Yaku


class MenzenTsumo(Yaku):
    def __init__(self) -> None:
        super().__init__("Menzen Tsumo", 1, 0)

    def hasYaku(self, ctx: HandContext) -> bool:
        return ctx.is_menzen and ctx.win_method == "tsumo"


__all__ = ["MenzenTsumo"]
