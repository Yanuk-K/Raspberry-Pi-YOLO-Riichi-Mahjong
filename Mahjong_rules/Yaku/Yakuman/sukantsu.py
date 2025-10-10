from Mahjong_rules.Yaku.utils import HandContext, Yaku


class SuuKantsu(Yaku):
    def __init__(self) -> None:
        super().__init__("Suu Kantsu", 13, 13)

    def hasYaku(self, ctx: HandContext) -> bool:
        return sum(1 for meld in ctx.melds if meld.is_quad()) >= 4


__all__ = ["SuuKantsu"]
