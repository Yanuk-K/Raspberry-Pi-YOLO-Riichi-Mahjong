from Mahjong_rules.Yaku.utils import HandContext, Yaku


class NagashiMangan(Yaku):
    def __init__(self) -> None:
        super().__init__("Nagashi Mangan", 5, 5)

    def hasYaku(self, ctx: HandContext) -> bool:
        return ctx.nagashi_mangan


__all__ = ["NagashiMangan"]
