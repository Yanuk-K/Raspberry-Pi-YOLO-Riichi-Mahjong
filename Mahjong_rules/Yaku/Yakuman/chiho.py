from Mahjong_rules.Yaku.utils import HandContext, Yaku


class Chiho(Yaku):
    def __init__(self) -> None:
        super().__init__("Chiho", 13, 13)

    def hasYaku(self, ctx: HandContext) -> bool:
        return ctx.blessing == "chiho"


__all__ = ["Chiho"]
