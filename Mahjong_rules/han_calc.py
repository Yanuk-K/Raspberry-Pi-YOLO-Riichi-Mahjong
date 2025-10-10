from __future__ import annotations

from typing import List, Optional, TypedDict

from Mahjong_rules.Yaku.utils import HandContext, HandPattern
from Mahjong_rules.has_yaku import evaluate_yaku, summarize_yaku, YakuResult


class HanSummary(TypedDict, total=False):
    han: int
    regular_han: int
    yakuman_count: int
    yaku: List[YakuResult]
    pattern: Optional[HandPattern]


def calculate_han(
    ctx: HandContext,
    *,
    include_ura: bool = False,
    include_red: bool = True,
    include_pei: bool = True,
    pattern: Optional[HandPattern] = None,
) -> HanSummary:
    results = evaluate_yaku(
        ctx,
        include_ura=include_ura,
        include_red=include_red,
        include_pei=include_pei,
        pattern=pattern,
    )
    yakuman_count, regular_han = summarize_yaku(results)
    effective_han = yakuman_count * 13 if yakuman_count else regular_han
    selected_pattern = (
        pattern if pattern is not None else ctx.additional_flags.get("yaku_pattern")
    )
    return HanSummary(
        han=effective_han,
        regular_han=regular_han,
        yakuman_count=yakuman_count,
        yaku=results,
        pattern=selected_pattern,
    )


__all__ = ["HanSummary", "calculate_han"]
