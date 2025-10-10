from __future__ import annotations

from typing import List, Optional, Tuple, TypedDict

from Mahjong_rules.Yaku.utils import HandContext, HandPattern
from Mahjong_rules.fu_calc import FuSummary, calculate_fu
from Mahjong_rules.has_yaku import (
    YakuResult,
    enumerate_yaku_results,
    summarize_yaku,
)


class TsumoDetail(TypedDict, total=False):
    dealer: int
    non_dealer: int
    non_dealer_count: int


class PointsDetail(TypedDict, total=False):
    ron: int
    tsumo: TsumoDetail
    total: int


class ScoreResult(TypedDict, total=False):
    han: int
    regular_han: int
    yakuman_count: int
    fu: int
    fu_raw: int
    fu_special: Optional[str]
    fu_breakdown: List[str]
    base_points: int
    limit: Optional[str]
    total_points: int
    points: PointsDetail
    is_dealer: bool
    pattern: Optional[HandPattern]
    yaku: List[YakuResult]


def _round_up_100(value: int) -> int:
    return ((value + 99) // 100) * 100


def _determine_limit(han: int, fu: int, yakuman_count: int) -> Tuple[int, Optional[str]]:
    if yakuman_count > 0:
        return 8000 * yakuman_count, "yakuman" if yakuman_count == 1 else f"{yakuman_count}x yakuman"
    if han >= 13:
        return 8000, "kazoe yakuman"
    if han >= 11:
        return 6000, "sanbaiman"
    if han >= 8:
        return 4000, "baiman"
    if han >= 6:
        return 3000, "haneman"
    if han >= 5:
        return 2000, "mangan"

    base_points = fu * (2 ** (2 + han))
    if base_points >= 2000:
        return 2000, "mangan"
    return base_points, None


def _points_for_hand(
    ctx: HandContext, base_points: int, is_dealer: bool
) -> Tuple[PointsDetail, int]:
    win_method = ctx.win_method or "ron"
    three_player = ctx.three_player

    if win_method == "ron":
        multiplier = 6 if is_dealer else 4
        amount = _round_up_100(base_points * multiplier)
        return PointsDetail(ron=amount, total=amount), amount

    if win_method == "tsumo":
        if is_dealer:
            share = _round_up_100(base_points * 2)
            payer_count = 2 if three_player else 3
            total = share * payer_count
            tsumo_detail: TsumoDetail = TsumoDetail(
                non_dealer=share,
                non_dealer_count=payer_count,
            )
            return PointsDetail(tsumo=tsumo_detail, total=total), total

        dealer_payment = _round_up_100(base_points * 2)
        non_dealer_share = _round_up_100(base_points)
        non_dealer_count = 1 if three_player else 2
        total = dealer_payment + non_dealer_share * non_dealer_count
        tsumo_detail = TsumoDetail(
            dealer=dealer_payment,
            non_dealer=non_dealer_share,
            non_dealer_count=non_dealer_count,
        )
        return PointsDetail(tsumo=tsumo_detail, total=total), total

    raise ValueError(f"Unknown win method: {ctx.win_method}")


def calculate_final_score(
    ctx: HandContext,
    *,
    include_ura: bool = False,
    include_red: bool = True,
    include_pei: bool = True,
) -> ScoreResult:
    is_dealer = ctx.seat_wind == "E"
    candidates = enumerate_yaku_results(
        ctx, include_ura=include_ura, include_red=include_red, include_pei=include_pei
    )

    best_result: Optional[ScoreResult] = None
    best_key: Tuple[int, int, int, int] = (-1, -1, -1, -1)

    for pattern, yaku_results in candidates:
        yakuman_count, regular_han = summarize_yaku(yaku_results)
        effective_han = yakuman_count * 13 if yakuman_count else regular_han
        if effective_han == 0:
            continue

        fu_summary: FuSummary = calculate_fu(ctx, pattern)
        fu = fu_summary["fu"]
        base_points, limit_name = _determine_limit(effective_han, fu, yakuman_count)
        points_detail, total_points = _points_for_hand(ctx, base_points, is_dealer)

        candidate: ScoreResult = ScoreResult(
            han=effective_han,
            regular_han=regular_han,
            yakuman_count=yakuman_count,
            fu=fu,
            fu_raw=fu_summary.get("raw", fu),
            fu_special=fu_summary.get("special"),
            fu_breakdown=fu_summary.get("breakdown", []),
            base_points=base_points,
            limit=limit_name,
            total_points=total_points,
            points=points_detail,
            is_dealer=is_dealer,
            pattern=pattern,
            yaku=yaku_results,
        )

        key = (total_points, yakuman_count, effective_han, fu)
        if best_result is None or key > best_key:
            best_result = candidate
            best_key = key

    if best_result is None:
        raise ValueError("Hand contains no valid yaku; cannot calculate score.")

    return best_result


__all__ = ["ScoreResult", "calculate_final_score"]
