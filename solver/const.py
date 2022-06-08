from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class ScoreConstant:
    """
    得点の評価に必要な定数をまとめたものである。
    """
    score_per_correct: float
    bonus_by_used_data: list[float]
    score_per_fail: float
