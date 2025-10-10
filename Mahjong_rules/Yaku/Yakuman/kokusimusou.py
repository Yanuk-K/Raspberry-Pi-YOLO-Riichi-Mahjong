from Mahjong_rules.Yaku.utils import HandContext, Yaku, is_kokushi


class KokushiMusou(Yaku):
    def __init__(self) -> None:
        super().__init__("Kokushi Musou", 13, 13)

    def hasYaku(self, ctx: HandContext) -> bool:
        return is_kokushi(ctx)


__all__ = ["KokushiMusou"]
