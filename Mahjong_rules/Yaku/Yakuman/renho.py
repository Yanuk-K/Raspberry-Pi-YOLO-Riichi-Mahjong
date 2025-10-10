from Mahjong_rules.Yaku.utils import HandContext, Yaku


class Renho(Yaku):
    def __init__(self) -> None:
        super().__init__("Renho", 13, 13)

    def hasYaku(self, ctx: HandContext) -> bool:
        return ctx.blessing == "renho"


__all__ = ["Renho"]
