from Mahjong_rules.Yaku.utils import HandContext, Yaku, concealed_triplet_count, has_tanki_wait


class SuankouTanki(Yaku):
    def __init__(self) -> None:
        super().__init__("Suankou Tanki", 13, 13)

    def hasYaku(self, ctx: HandContext) -> bool:
        for pattern in ctx.enumerate_patterns():
            if concealed_triplet_count(ctx, pattern) == 4 and has_tanki_wait(ctx, pattern):
                return True
        return False


__all__ = ["SuankouTanki"]
