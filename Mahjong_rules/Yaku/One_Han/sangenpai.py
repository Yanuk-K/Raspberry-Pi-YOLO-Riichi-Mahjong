from Mahjong_rules.Yaku.utils import HandContext, Yaku

DRAGON_KEYS = {"haku": "P", "hatsu": "F", "chun": "C"}


def has_dragon_triplet(ctx: HandContext, dragon_key: str) -> bool:
    for pattern in ctx.enumerate_patterns():
        for meld in pattern.all_melds():
            if not meld.is_triplet():
                continue
            if all(key == dragon_key for key in meld.tile_keys):
                return True
    return False


class DragonYakuhai(Yaku):
    def __init__(self, name: str, dragon_key: str) -> None:
        super().__init__(name, 1, 1)
        self.dragon_key = dragon_key

    def hasYaku(self, ctx: HandContext) -> bool:
        return has_dragon_triplet(ctx, self.dragon_key)


__all__ = ["DragonYakuhai", "DRAGON_KEYS", "has_dragon_triplet"]
