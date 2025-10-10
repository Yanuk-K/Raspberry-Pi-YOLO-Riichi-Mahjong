from Mahjong_rules.Yaku.utils import HandContext, Yaku


class Renpuuhai(Yaku):
    def __init__(self) -> None:
        super().__init__("Renpuuhai", 2, 2)

    def hasYaku(self, ctx: HandContext) -> bool:
        if ctx.seat_wind != ctx.round_wind:
            return False
        target = ctx.seat_wind
        for pattern in ctx.enumerate_patterns():
            for meld in pattern.all_melds():
                if not meld.is_triplet():
                    continue
                if all(key == target for key in meld.tile_keys):
                    return True
        return False


__all__ = ["Renpuuhai"]
