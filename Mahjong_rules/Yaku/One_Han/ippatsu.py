from Mahjong_rules.Yaku.utils import HandContext, Yaku


class Ippatsu(Yaku):
    def __init__(self) -> None:
        super().__init__("Ippatsu", 1, 1)

    def hasYaku(self, ctx: HandContext) -> bool:
        return ctx.ippatsu and ctx.riichi


__all__ = ["Ippatsu"]
