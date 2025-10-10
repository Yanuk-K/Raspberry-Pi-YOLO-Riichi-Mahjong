from Mahjong_rules.Yaku.utils import HandContext, Yaku, key_is_terminal_or_honor


class Honroutou(Yaku):
    def __init__(self) -> None:
        super().__init__("Honroutou", 2, 2)

    def hasYaku(self, ctx: HandContext) -> bool:
        for key in ctx.tile_counter:
            if not key_is_terminal_or_honor(key):
                return False
        return True


__all__ = ["Honroutou"]
