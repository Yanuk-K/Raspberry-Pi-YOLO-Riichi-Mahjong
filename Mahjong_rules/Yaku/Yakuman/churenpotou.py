from Mahjong_rules.Yaku.utils import HandContext, Yaku, analyze_churen


class ChurenPotou(Yaku):
    def __init__(self) -> None:
        super().__init__("Churen Poutou", 13, 13)

    def hasYaku(self, ctx: HandContext) -> bool:
        if not ctx.is_menzen:
            return False
        return analyze_churen(ctx) is not None


__all__ = ["ChurenPotou"]
