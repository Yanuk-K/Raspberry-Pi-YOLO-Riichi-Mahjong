from __future__ import annotations

from typing import List, Optional, TypedDict

from Mahjong_rules.Yaku.utils import (
    HandContext,
    HandPattern,
    VALUE_HONOR_KEYS,
    determine_wait_kind,
    is_chiitoitsu,
    is_pinfu_pattern,
    key_is_terminal_or_honor,
)


class FuSummary(TypedDict, total=False):
    fu: int
    raw: int
    breakdown: List[str]
    pattern: Optional[HandPattern]
    special: Optional[str]


def _round_fu(value: int) -> int:
    return ((value + 9) // 10) * 10


def _pair_fu(ctx: HandContext, pattern: HandPattern, breakdown: List[str]) -> int:
    pair_key = pattern.pair.tile_keys[0]
    fu = 0
    if pair_key == ctx.seat_wind:
        fu += 2
    if pair_key == ctx.round_wind:
        fu += 2
    if pair_key in VALUE_HONOR_KEYS:
        fu += 2
    if fu:
        breakdown.append(f"Value pair +{fu}")
    return fu


def _triplet_fu(pattern: HandPattern, breakdown: List[str]) -> int:
    total = 0
    for meld in pattern.all_melds():
        if not meld.is_triplet():
            continue
        tile_key = meld.tile_keys[0]
        is_valuable = key_is_terminal_or_honor(tile_key)
        if meld.is_quad():
            base = 8 if meld.is_open else 16
            label = "Open kan" if meld.is_open else "Closed kan"
        else:
            base = 2 if meld.is_open else 4
            label = "Open triplet" if meld.is_open else "Closed triplet"
        if is_valuable:
            base *= 2
            label += " (terminal/honor)"
        else:
            label += " (simple)"
        total += base
        breakdown.append(f"{label} +{base}")
    return total


def _wait_fu(ctx: HandContext, pattern: HandPattern, breakdown: List[str]) -> int:
    wait_kind = determine_wait_kind(ctx, pattern)
    if wait_kind in {"tanki", "kanchan", "penchan"}:
        breakdown.append(f"Wait ({wait_kind}) +2")
        return 2
    return 0


def _fu_for_pattern(ctx: HandContext, pattern: HandPattern) -> FuSummary:
    if is_pinfu_pattern(ctx, pattern) and ctx.win_method == "tsumo":
        return FuSummary(
            fu=20,
            raw=20,
            breakdown=["Pinfu tsumo fixed 20 fu"],
            pattern=pattern,
            special="pinfu_tsumo",
        )

    breakdown: List[str] = ["Base 20"]
    raw_fu = 20

    if ctx.win_method == "tsumo":
        raw_fu += 2
        breakdown.append("Tsumo +2")

    if ctx.is_menzen and ctx.win_method == "ron":
        raw_fu += 10
        breakdown.append("Menzen ron +10")

    raw_fu += _pair_fu(ctx, pattern, breakdown)
    raw_fu += _triplet_fu(pattern, breakdown)
    raw_fu += _wait_fu(ctx, pattern, breakdown)

    fu = _round_fu(raw_fu)
    if fu != raw_fu:
        breakdown.append(f"Rounded to {fu}")

    return FuSummary(fu=fu, raw=raw_fu, breakdown=breakdown, pattern=pattern)


def calculate_fu(ctx: HandContext, pattern: Optional[HandPattern] = None) -> FuSummary:
    if is_chiitoitsu(ctx):
        return FuSummary(
            fu=25,
            raw=25,
            breakdown=["Chiitoitsu fixed 25 fu"],
            pattern=None,
            special="chiitoitsu",
        )

    patterns = ctx.enumerate_patterns()
    if not patterns:
        # Fallback for special hands like kokushi; fu does not affect yakuman scoring.
        base = 20
        breakdown = ["Base 20"]
        if ctx.win_method == "tsumo":
            base += 2
            breakdown.append("Tsumo +2")
        if ctx.is_menzen and ctx.win_method == "ron":
            base += 10
            breakdown.append("Menzen ron +10")
        fu = _round_fu(base)
        if fu != base:
            breakdown.append(f"Rounded to {fu}")
        return FuSummary(fu=fu, raw=base, breakdown=breakdown, pattern=None)

    if pattern is not None:
        return _fu_for_pattern(ctx, pattern)

    best_summary: Optional[FuSummary] = None
    for candidate in patterns:
        summary = _fu_for_pattern(ctx, candidate)
        if best_summary is None or summary["fu"] > best_summary["fu"]:
            best_summary = summary

    assert best_summary is not None
    return best_summary


__all__ = ["FuSummary", "calculate_fu"]
