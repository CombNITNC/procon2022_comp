from solver.card import ShouldPickCardsByProblem
from solver.const import ScoreConstant
from solver.state import SolverState


def current_score(
    state: SolverState,
    should_picks: ShouldPickCardsByProblem,
    const: ScoreConstant,
) -> float:
    """
    現在の回答状況からスコアを計算する。
    """
    point = 0.0
    for problem in should_picks.problems():
        picks = should_picks.picks_on(problem)
        point += picks * const.score_per_correct * \
            const.bonus_by_used_data[state.used_chunks[problem]]
    point -= state.current_fails * const.score_per_fail
    return point


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
