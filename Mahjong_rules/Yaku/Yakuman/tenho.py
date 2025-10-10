from Mahjong_rules.Yaku.utils import HandContext, Yaku


class Tenho(Yaku):
    def __init__(self) -> None:
        super().__init__("Tenho", 13, 13)

    def hasYaku(self, ctx: HandContext) -> bool:
        return ctx.blessing == "tenho"


__all__ = ["Tenho"]
