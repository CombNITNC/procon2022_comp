from solver.const import ScoreConstant


def calc_score(
    corrects: int,
    fails: int,
    used_data: int,
    const: ScoreConstant
) -> float:
    """
    正解数、お手付きの数、使用した分割データの数から得点を算出する。
    """
    point = corrects * const.score_per_correct * \
        const.bonus_by_used_data[used_data]
    deduct = fails * const.score_per_fail
    return point - deduct
