from Mahjong_rules.Yaku.utils import HandContext, Yaku, is_honitsu


class Honitsu(Yaku):
    def __init__(self) -> None:
        super().__init__("Honitsu", 3, 2)

    def hasYaku(self, ctx: HandContext) -> bool:
        return is_honitsu(ctx)


__all__ = ["Honitsu"]
