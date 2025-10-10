from Mahjong_rules.Yaku.utils import HandContext, Yaku, triplets_by_suit


class SanshokuDoukou(Yaku):
    def __init__(self) -> None:
        super().__init__("Sanshoku Doukou", 2, 2)

    def hasYaku(self, ctx: HandContext) -> bool:
        for pattern in ctx.enumerate_patterns():
            by_suit = triplets_by_suit(pattern)
            for value in map(str, range(1, 10)):
                if all(value in by_suit.get(suit, []) for suit in ("m", "p", "s")):
                    return True
        return False


__all__ = ["SanshokuDoukou"]
