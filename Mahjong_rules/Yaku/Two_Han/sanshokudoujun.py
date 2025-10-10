from Mahjong_rules.Yaku.utils import HandContext, Yaku, sequences_by_suit


class SanshokuDoujun(Yaku):
    def __init__(self) -> None:
        super().__init__("Sanshoku Doujun", 2, 1)

    def hasYaku(self, ctx: HandContext) -> bool:
        for pattern in ctx.enumerate_patterns():
            by_suit = sequences_by_suit(pattern)
            for start in range(1, 8):
                if all(start in by_suit.get(suit, []) for suit in ("m", "p", "s")):
                    return True
        return False


__all__ = ["SanshokuDoujun"]
