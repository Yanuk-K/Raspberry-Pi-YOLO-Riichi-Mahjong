from collections import Counter
from typing import Iterable

from Mahjong_rules.Yaku.utils import HandContext, indicator_to_tile


def _count_from_indicators(ctx: HandContext, indicators: Iterable) -> int:
    if not indicators:
        return 0
    indicator_targets = Counter(
        indicator_to_tile(indicator).key for indicator in indicators
    )
    total = 0
    for key, multiplier in indicator_targets.items():
        total += ctx.tile_counter.get(key, 0) * multiplier
    return total


def count_dora(
    ctx: HandContext,
    include_ura: bool = False,
    include_red: bool = True,
    include_pei: bool = True,
) -> int:
    total = 0
    total += _count_from_indicators(
        ctx, list(ctx.dora_indicators) + list(ctx.kan_dora_indicators)
    )
    if include_ura:
        total += _count_from_indicators(
            ctx, list(ctx.ura_dora_indicators) + list(ctx.kan_ura_dora_indicators)
        )
    if include_red:
        total += ctx.red_tile_count()
    if include_pei:
        total += ctx.pei_nuki_count
    total += ctx.additional_flags.get("extra_dora", 0)
    return total


__all__ = ["count_dora"]
