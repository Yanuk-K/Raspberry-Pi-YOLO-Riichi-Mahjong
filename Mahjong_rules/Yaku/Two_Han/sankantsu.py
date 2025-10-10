from Mahjong_rules.Yaku.utils import HandContext, Yaku


class SanKantsu(Yaku):
    def __init__(self) -> None:
        super().__init__("San Kantsu", 2, 2)

    def hasYaku(self, ctx: HandContext) -> bool:
        return sum(1 for meld in ctx.melds if meld.is_quad()) >= 3


__all__ = ["SanKantsu"]
