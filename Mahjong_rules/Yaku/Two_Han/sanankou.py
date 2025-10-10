from Mahjong_rules.Yaku.utils import HandContext, Yaku, concealed_triplet_count


class SanAnkou(Yaku):
    def __init__(self) -> None:
        super().__init__("San Ankou", 2, 2)

    def hasYaku(self, ctx: HandContext) -> bool:
        for pattern in ctx.enumerate_patterns():
            if concealed_triplet_count(ctx, pattern) >= 3:
                return True
        return False


__all__ = ["SanAnkou"]
