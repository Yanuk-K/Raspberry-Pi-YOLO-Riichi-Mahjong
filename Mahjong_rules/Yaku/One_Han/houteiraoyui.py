from Mahjong_rules.Yaku.utils import HandContext, Yaku


class HouteiRaoyui(Yaku):
    def __init__(self) -> None:
        super().__init__("Houtei Raoyui", 1, 1)

    def hasYaku(self, ctx: HandContext) -> bool:
        return ctx.is_houtei and ctx.win_method == "ron"


__all__ = ["HouteiRaoyui"]
