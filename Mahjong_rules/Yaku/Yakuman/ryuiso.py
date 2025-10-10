from Mahjong_rules.Yaku.utils import GREEN_TILE_KEYS, HandContext, Yaku


class Ryuuiso(Yaku):
    def __init__(self) -> None:
        super().__init__("Ryuuiso", 13, 13)

    def hasYaku(self, ctx: HandContext) -> bool:
        for key in ctx.tile_counter:
            if key not in GREEN_TILE_KEYS:
                return False
        return True


__all__ = ["Ryuuiso"]
