from Mahjong_rules.Yaku.utils import (
    HandContext,
    Yaku,
    TERMINAL_KEYS,
    key_is_terminal,
    suitedness,
    sequence_signature,
)


class Junchan(Yaku):
    def __init__(self) -> None:
        super().__init__("Junchan", 3, 2)

    def hasYaku(self, ctx: HandContext) -> bool:
        if "z" in suitedness(ctx):
            return False

        for pattern in ctx.enumerate_patterns():
            pair_key = pattern.pair.tile_keys[0]
            if not key_is_terminal(pair_key):
                continue
            has_sequence = False
            valid = True
            for meld in pattern.all_melds():
                if meld.is_sequence():
                    has_sequence = True
                    suit, start = sequence_signature(meld)
                    if start not in {1, 7}:
                        valid = False
                        break
                else:
                    tile_key = meld.tile_keys[0]
                    if tile_key not in TERMINAL_KEYS:
                        valid = False
                        break
            if valid and has_sequence:
                return True
        return False


__all__ = ["Junchan"]
