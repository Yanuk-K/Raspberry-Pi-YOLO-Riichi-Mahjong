from Mahjong_rules.Yaku.Yakuman.daisusi import WINDS
from Mahjong_rules.Yaku.utils import HandContext, Yaku


class Shousushi(Yaku):
    def __init__(self) -> None:
        super().__init__("Shousushi", 13, 13)

    def hasYaku(self, ctx: HandContext) -> bool:
        for pattern in ctx.enumerate_patterns():
            wind_triplets = {
                meld.tile_keys[0]
                for meld in pattern.all_melds()
                if meld.is_triplet() and meld.tile_keys[0] in WINDS
            }
            if len(wind_triplets) != 3:
                continue
            pair_key = pattern.pair.tile_keys[0]
            if pair_key in WINDS and pair_key not in wind_triplets:
                return True
        return False


__all__ = ["Shousushi"]
