from Mahjong_rules.Yaku.utils import HandContext, Yaku, analyze_churen


class JunseiChurenPotou(Yaku):
    def __init__(self) -> None:
        super().__init__("Junsei Churen Poutou", 13, 13)

    def hasYaku(self, ctx: HandContext) -> bool:
        if not ctx.is_menzen or ctx.winning_tile is None:
            return False
        analysis = analyze_churen(ctx)
        if not analysis:
            return False
        suit, extra_value = analysis
        return (
            ctx.winning_tile.suit == suit
            and ctx.winning_tile.value == extra_value
        )


__all__ = ["JunseiChurenPotou"]
