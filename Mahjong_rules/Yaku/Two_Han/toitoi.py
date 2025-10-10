from Mahjong_rules.Yaku.utils import HandContext, Yaku


class Toitoi(Yaku):
    def __init__(self) -> None:
        super().__init__("Toitoi", 2, 2)

    def hasYaku(self, ctx: HandContext) -> bool:
        for pattern in ctx.enumerate_patterns():
            if all(meld.is_triplet() for meld in pattern.all_melds()):
                return True
        return False


__all__ = ["Toitoi"]
