from Mahjong_rules.Yaku.utils import (
    HandContext,
    Yaku,
    key_is_terminal_or_honor,
    sequence_signature,
)


class Chanta(Yaku):
    def __init__(self) -> None:
        super().__init__("Chanta", 2, 1)

    def hasYaku(self, ctx: HandContext) -> bool:
        for pattern in ctx.enumerate_patterns():
            pair_key = pattern.pair.tile_keys[0]
            if not key_is_terminal_or_honor(pair_key):
                continue
            has_sequence = False
            valid = True
            for meld in pattern.all_melds():
                if meld.is_sequence():
                    has_sequence = True
                    suit, start = sequence_signature(meld)
                    if suit not in {"m", "p", "s"} or start not in {1, 7}:
                        valid = False
                        break
                else:
                    tile_key = meld.tile_keys[0]
                    if not key_is_terminal_or_honor(tile_key):
                        valid = False
                        break
            if valid and has_sequence:
                return True
        return False


__all__ = ["Chanta"]
