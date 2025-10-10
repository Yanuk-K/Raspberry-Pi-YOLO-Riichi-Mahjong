from Mahjong_rules.Yaku.utils import HandContext, Yaku

WINDS = {"E", "S", "W", "N"}


class Daisushi(Yaku):
    def __init__(self) -> None:
        super().__init__("Daisushi", 13, 13)

    def hasYaku(self, ctx: HandContext) -> bool:
        for pattern in ctx.enumerate_patterns():
            wind_triplets = {
                meld.tile_keys[0]
                for meld in pattern.all_melds()
                if meld.is_triplet() and meld.tile_keys[0] in WINDS
            }
            if WINDS.issubset(wind_triplets):
                return True
        return False


__all__ = ["Daisushi"]
