from Mahjong_rules.Yaku.utils import HandContext, TERMINAL_KEYS, Yaku


class Chinroutou(Yaku):
    def __init__(self) -> None:
        super().__init__("Chinroutou", 13, 13)

    def hasYaku(self, ctx: HandContext) -> bool:
        for key in ctx.tile_counter:
            if key not in TERMINAL_KEYS:
                return False
        return True


__all__ = ["Chinroutou"]
