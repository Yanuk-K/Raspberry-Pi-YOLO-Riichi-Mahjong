from Mahjong_rules.Yaku.One_Han.sangenpai import DRAGON_KEYS
from Mahjong_rules.Yaku.utils import HandContext, Yaku

DRAGON_SET = set(DRAGON_KEYS.values())


class Shousangen(Yaku):
    def __init__(self) -> None:
        super().__init__("Shousangen", 2, 2)

    def hasYaku(self, ctx: HandContext) -> bool:
        for pattern in ctx.enumerate_patterns():
            dragon_triplets = {
                meld.tile_keys[0]
                for meld in pattern.all_melds()
                if meld.is_triplet() and meld.tile_keys[0] in DRAGON_SET
            }
            if len(dragon_triplets) != 2:
                continue
            pair_key = pattern.pair.tile_keys[0]
            if pair_key in DRAGON_SET and pair_key not in dragon_triplets:
                return True
        return False


__all__ = ["Shousangen"]
