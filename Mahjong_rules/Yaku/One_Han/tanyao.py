from Mahjong_rules.Yaku.utils import HandContext, Yaku, key_is_simple


class Tanyao(Yaku):
    def __init__(self) -> None:
        super().__init__("Tanyao", 1, 1)

    def hasYaku(self, ctx: HandContext) -> bool:
        for key in ctx.tile_counter:
            if not key_is_simple(key):
                return False
        return True


__all__ = ["Tanyao"]
