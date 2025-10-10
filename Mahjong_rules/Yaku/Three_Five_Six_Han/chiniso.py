from Mahjong_rules.Yaku.utils import HandContext, Yaku, is_chinitsu


class Chinitsu(Yaku):
    def __init__(self) -> None:
        super().__init__("Chinitsu", 6, 5)

    def hasYaku(self, ctx: HandContext) -> bool:
        return is_chinitsu(ctx)


__all__ = ["Chinitsu"]
