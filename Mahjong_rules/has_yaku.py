from __future__ import annotations

from typing import List, Optional, Tuple, TypedDict

from Mahjong_rules.Yaku.One_Han.chankan import Chankan
from Mahjong_rules.Yaku.One_Han.haiteirauyuu import HaiteiRaoyue
from Mahjong_rules.Yaku.One_Han.houteiraoyui import HouteiRaoyui
from Mahjong_rules.Yaku.One_Han.iipeiko import Iipeiko
from Mahjong_rules.Yaku.One_Han.ippatsu import Ippatsu
from Mahjong_rules.Yaku.One_Han.kazehai import Kazehai
from Mahjong_rules.Yaku.One_Han.menzen_tsumo import MenzenTsumo
from Mahjong_rules.Yaku.One_Han.pinfu import Pinfu
from Mahjong_rules.Yaku.One_Han.riichi import Riichi
from Mahjong_rules.Yaku.One_Han.rinshankaihou import RinshanKaihou
from Mahjong_rules.Yaku.One_Han.Sangenpai.chun import Chun
from Mahjong_rules.Yaku.One_Han.Sangenpai.haku import Haku
from Mahjong_rules.Yaku.One_Han.Sangenpai.hatsu import Hatsu
from Mahjong_rules.Yaku.One_Han.tanyao import Tanyao
from Mahjong_rules.Yaku.Three_Five_Six_Han.chiniso import Chinitsu
from Mahjong_rules.Yaku.Three_Five_Six_Han.honiso import Honitsu
from Mahjong_rules.Yaku.Three_Five_Six_Han.junchan import Junchan
from Mahjong_rules.Yaku.Three_Five_Six_Han.nagasimangan import NagashiMangan
from Mahjong_rules.Yaku.Three_Five_Six_Han.ryanpeiko import Ryanpeiko
from Mahjong_rules.Yaku.Two_Han.chanta import Chanta
from Mahjong_rules.Yaku.Two_Han.chiitoitsu import Chiitoitsu
from Mahjong_rules.Yaku.Two_Han.daburi import DaburuRiichi
from Mahjong_rules.Yaku.Two_Han.honroutou import Honroutou
from Mahjong_rules.Yaku.Two_Han.ikkitsuukan import Ikkitsuukan
from Mahjong_rules.Yaku.Two_Han.renpuuhai import Renpuuhai
from Mahjong_rules.Yaku.Two_Han.sanankou import SanAnkou
from Mahjong_rules.Yaku.Two_Han.sankantsu import SanKantsu
from Mahjong_rules.Yaku.Two_Han.sanshokudoujun import SanshokuDoujun
from Mahjong_rules.Yaku.Two_Han.sanshokudoukou import SanshokuDoukou
from Mahjong_rules.Yaku.Two_Han.shousangen import Shousangen
from Mahjong_rules.Yaku.Two_Han.toitoi import Toitoi
from Mahjong_rules.Yaku.Yakuman.chiho import Chiho
from Mahjong_rules.Yaku.Yakuman.chinroutou import Chinroutou
from Mahjong_rules.Yaku.Yakuman.churenpotou import ChurenPotou
from Mahjong_rules.Yaku.Yakuman.daisangen import Daisangen
from Mahjong_rules.Yaku.Yakuman.daisusi import Daisushi
from Mahjong_rules.Yaku.Yakuman.junseicyurenpotou import JunseiChurenPotou
from Mahjong_rules.Yaku.Yakuman.kokusimusou import KokushiMusou
from Mahjong_rules.Yaku.Yakuman.kokusimusoujusanmenmachi import (
    KokushiMusouThirteenWait,
)
from Mahjong_rules.Yaku.Yakuman.renho import Renho
from Mahjong_rules.Yaku.Yakuman.ryuiso import Ryuuiso
from Mahjong_rules.Yaku.Yakuman.shoususi import Shousushi
from Mahjong_rules.Yaku.Yakuman.suankou import Suankou
from Mahjong_rules.Yaku.Yakuman.suankotanki import SuankouTanki
from Mahjong_rules.Yaku.Yakuman.sukantsu import SuuKantsu
from Mahjong_rules.Yaku.Yakuman.tenho import Tenho
from Mahjong_rules.Yaku.Yakuman.tsuiso import Tsuiso
from Mahjong_rules.Yaku.dora import count_dora
from Mahjong_rules.Yaku.utils import HandContext, HandPattern, Yaku


class YakuResult(TypedDict):
    name: str
    han: int
    yakuman: bool


MENZEN_TSUMO = MenzenTsumo()
RIICHI = Riichi()
IPPATSU = Ippatsu()
PINFU = Pinfu()
TANYAO = Tanyao()
IIPEIKO = Iipeiko()
CHANKAN = Chankan()
RINSHAN = RinshanKaihou()
HAITEI = HaiteiRaoyue()
HOUTEI = HouteiRaoyui()
SEAT_WIND = Kazehai("seat")
ROUND_WIND = Kazehai("round")
CHUN = Chun()
HATSU = Hatsu()
HAKU = Haku()
CHIITOITSU = Chiitoitsu()
CHANTA = Chanta()
DABURU_RIICHI = DaburuRiichi()
HONROUTOU = Honroutou()
IKKITSUUKAN = Ikkitsuukan()
RENPUUHAI = Renpuuhai()
SANANKOU = SanAnkou()
SANKANTSU = SanKantsu()
SANSHOKU_DOUJUN = SanshokuDoujun()
SANSHOKU_DOUKOU = SanshokuDoukou()
SHOUSANGEN = Shousangen()
TOITOI = Toitoi()
HONITSU = Honitsu()
CHINITSU = Chinitsu()
JUNCHAN = Junchan()
RYANPEIKO = Ryanpeiko()
NAGASHI_MANGAN = NagashiMangan()
CHINROUTOU = Chinroutou()
TSUISO = Tsuiso()
RYUISO = Ryuuiso()
DAISANGEN = Daisangen()
DAISUSHI = Daisushi()
SHOUSUSHI = Shousushi()
SUANKOU = Suankou()
SUANKOU_TANKI = SuankouTanki()
SUU_KANTSU = SuuKantsu()
KOKUSHI = KokushiMusou()
KOKUSHI_13 = KokushiMusouThirteenWait()
CHUREN = ChurenPotou()
JUNSEI_CHUREN = JunseiChurenPotou()
CHIHO_YAKU = Chiho()
TENHO_YAKU = Tenho()
RENHO_YAKU = Renho()

ALL_YAKU: List[Yaku] = [
    MENZEN_TSUMO,
    RIICHI,
    IPPATSU,
    PINFU,
    TANYAO,
    IIPEIKO,
    CHANKAN,
    RINSHAN,
    HAITEI,
    HOUTEI,
    SEAT_WIND,
    ROUND_WIND,
    CHUN,
    HATSU,
    HAKU,
    CHIITOITSU,
    CHANTA,
    DABURU_RIICHI,
    HONROUTOU,
    IKKITSUUKAN,
    RENPUUHAI,
    SANANKOU,
    SANKANTSU,
    SANSHOKU_DOUJUN,
    SANSHOKU_DOUKOU,
    SHOUSANGEN,
    TOITOI,
    HONITSU,
    CHINITSU,
    JUNCHAN,
    RYANPEIKO,
    NAGASHI_MANGAN,
    CHINROUTOU,
    TSUISO,
    RYUISO,
    DAISANGEN,
    DAISUSHI,
    SHOUSUSHI,
    SUANKOU,
    SUANKOU_TANKI,
    SUU_KANTSU,
    KOKUSHI,
    KOKUSHI_13,
    CHUREN,
    JUNSEI_CHUREN,
    CHIHO_YAKU,
    TENHO_YAKU,
    RENHO_YAKU,
]

GLOBAL_YAKU: List[Yaku] = [
    MENZEN_TSUMO,
    RIICHI,
    DABURU_RIICHI,
    IPPATSU,
    CHANKAN,
    RINSHAN,
    HAITEI,
    HOUTEI,
    TANYAO,
    CHIITOITSU,
    HONROUTOU,
    SANKANTSU,
    HONITSU,
    CHINITSU,
    NAGASHI_MANGAN,
    CHINROUTOU,
    TSUISO,
    RYUISO,
    SUU_KANTSU,
    KOKUSHI,
    KOKUSHI_13,
    CHUREN,
    JUNSEI_CHUREN,
    CHIHO_YAKU,
    TENHO_YAKU,
    RENHO_YAKU,
]

PATTERN_YAKU: List[Yaku] = [yaku for yaku in ALL_YAKU if yaku not in GLOBAL_YAKU]


def _collect_global_yaku(ctx: HandContext, menzen: bool) -> List[YakuResult]:
    results: List[YakuResult] = []
    for yaku in GLOBAL_YAKU:
        score = yaku.yakuScore(ctx, menzen)
        if score:
            results.append({"name": yaku.name, "han": score, "yakuman": yaku.is_yakuman})
    return results


def _collect_pattern_yaku(
    ctx: HandContext, menzen: bool, pattern: Optional[HandPattern]
) -> List[YakuResult]:
    if pattern is None:
        return []
    original_cache = ctx._pattern_cache
    results: List[YakuResult] = []
    try:
        ctx._pattern_cache = [pattern]
        for yaku in PATTERN_YAKU:
            score = yaku.yakuScore(ctx, menzen)
            if score:
                results.append({"name": yaku.name, "han": score, "yakuman": yaku.is_yakuman})
    finally:
        ctx._pattern_cache = original_cache
    return results


def summarize_yaku(results: List[YakuResult]) -> Tuple[int, int]:
    yakuman_count = 0
    regular_han = 0
    for entry in results:
        if entry["yakuman"]:
            yakuman_count += entry["han"] // 13 if entry["han"] >= 13 else 1
        else:
            regular_han += entry["han"]
    return yakuman_count, regular_han


def _evaluation_key(results: List[YakuResult]) -> Tuple[int, int, int]:
    yakuman_count, regular_han = summarize_yaku(results)
    return yakuman_count, regular_han, len(results)


def _append_dora(
    ctx: HandContext,
    results: List[YakuResult],
    include_ura: bool,
    include_red: bool,
    include_pei: bool,
) -> List[YakuResult]:
    dora_han = count_dora(
        ctx, include_ura=include_ura, include_red=include_red, include_pei=include_pei
    )
    if dora_han:
        results = list(results)
        results.append({"name": "Dora", "han": dora_han, "yakuman": False})
    return results


def evaluate_yaku(
    ctx: HandContext,
    *,
    include_ura: bool = False,
    include_red: bool = True,
    include_pei: bool = True,
    pattern: Optional[HandPattern] = None,
) -> List[YakuResult]:
    menzen = ctx.is_menzen
    global_results = _collect_global_yaku(ctx, menzen)

    if pattern is not None:
        pattern_results = _collect_pattern_yaku(ctx, menzen, pattern)
        combined = global_results + pattern_results
        ctx.additional_flags["yaku_pattern"] = pattern
        return _append_dora(ctx, combined, include_ura, include_red, include_pei)

    patterns = ctx.enumerate_patterns()
    if not patterns:
        ctx.additional_flags["yaku_pattern"] = None
        combined = global_results
        return _append_dora(ctx, combined, include_ura, include_red, include_pei)

    best_pattern: Optional[HandPattern] = None
    best_results: List[YakuResult] = []
    best_key: Tuple[int, int, int] = (-1, -1, -1)

    for candidate in patterns:
        pattern_results = _collect_pattern_yaku(ctx, menzen, candidate)
        combined = global_results + pattern_results
        key = _evaluation_key(combined)
        if key > best_key:
            best_key = key
            best_pattern = candidate
            best_results = pattern_results

    ctx.additional_flags["yaku_pattern"] = best_pattern
    final_results = global_results + best_results
    return _append_dora(ctx, final_results, include_ura, include_red, include_pei)


def enumerate_yaku_results(
    ctx: HandContext,
    *,
    include_ura: bool = False,
    include_red: bool = True,
    include_pei: bool = True,
) -> List[Tuple[Optional[HandPattern], List[YakuResult]]]:
    menzen = ctx.is_menzen
    patterns = ctx.enumerate_patterns()
    results: List[Tuple[Optional[HandPattern], List[YakuResult]]] = []

    if not patterns:
        combined = _append_dora(
            ctx,
            _collect_global_yaku(ctx, menzen),
            include_ura,
            include_red,
            include_pei,
        )
        results.append((None, combined))
        return results

    for pattern in patterns:
        global_results = _collect_global_yaku(ctx, menzen)
        pattern_results = _collect_pattern_yaku(ctx, menzen, pattern)
        combined = global_results + pattern_results
        combined = _append_dora(ctx, combined, include_ura, include_red, include_pei)
        results.append((pattern, combined))
    return results


def total_han(
    ctx: HandContext,
    *,
    include_ura: bool = False,
    include_red: bool = True,
    include_pei: bool = True,
) -> int:
    results = evaluate_yaku(
        ctx,
        include_ura=include_ura,
        include_red=include_red,
        include_pei=include_pei,
    )
    yakuman_count, regular_han = summarize_yaku(results)
    return regular_han if yakuman_count == 0 else yakuman_count * 13


__all__ = [
    "ALL_YAKU",
    "evaluate_yaku",
    "enumerate_yaku_results",
    "summarize_yaku",
    "total_han",
]
