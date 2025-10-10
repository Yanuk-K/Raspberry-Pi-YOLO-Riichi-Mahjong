from Mahjong_rules.Yaku.utils import HandContext, HONOR_KEYS, Yaku


class Tsuiso(Yaku):
    def __init__(self) -> None:
        super().__init__("Tsuiso", 13, 13)

    def hasYaku(self, ctx: HandContext) -> bool:
        for key in ctx.tile_counter:
            if key not in HONOR_KEYS:
                return False
        return True


__all__ = ["Tsuiso"]
