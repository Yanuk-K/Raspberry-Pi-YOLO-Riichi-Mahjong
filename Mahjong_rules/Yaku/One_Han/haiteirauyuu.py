from Mahjong_rules.Yaku.utils import HandContext, Yaku


class HaiteiRaoyue(Yaku):
    def __init__(self) -> None:
        super().__init__("Haitei Raoyue", 1, 1)

    def hasYaku(self, ctx: HandContext) -> bool:
        return ctx.is_haitei and ctx.win_method == "tsumo"


__all__ = ["HaiteiRaoyue"]
