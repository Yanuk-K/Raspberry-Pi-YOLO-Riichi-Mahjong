from Mahjong_rules.Yaku.utils import HandContext, Yaku, is_kokushi_thirteen_wait


class KokushiMusouThirteenWait(Yaku):
    def __init__(self) -> None:
        super().__init__("Kokushi Musou 13-Sided Wait", 13, 13)

    def hasYaku(self, ctx: HandContext) -> bool:
        return is_kokushi_thirteen_wait(ctx)


__all__ = ["KokushiMusouThirteenWait"]
