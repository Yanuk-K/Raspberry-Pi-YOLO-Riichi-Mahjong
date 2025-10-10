from Mahjong_rules.Yaku.utils import HandContext, Yaku, sequences_by_suit


class Ikkitsuukan(Yaku):
    def __init__(self) -> None:
        super().__init__("Ikkitsuukan", 2, 1)

    def hasYaku(self, ctx: HandContext) -> bool:
        for pattern in ctx.enumerate_patterns():
            by_suit = sequences_by_suit(pattern)
            for suit in ("m", "p", "s"):
                starts = set(by_suit.get(suit, []))
                if {1, 4, 7}.issubset(starts):
                    return True
        return False


__all__ = ["Ikkitsuukan"]
