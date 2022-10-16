import abc
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class Match:
    """試合全体を通して変化しない、問題全体で共通の情報。

    試合全体を通して、同じ取り札は日本語か英語かに関わらず 1 度までしか登場しない。例えば、E01 がすでに読み上げられた場合は J01 は登場しない。

    Attributes:
        problems (int): 試合中の問題数。
        bonus_factor (list[float]): スコア計算のボーナス係数のリスト。
            使用した分割数 n 個に対して n 番目の係数が適用される。
        penalty (int): 変更札である取り札のスコアに対して適用される係数。
    """
    problems: int
    bonus_factor: list[float]
    penalty: int
    change_penalty: int
    wrong_penalty: int
    correct_point: int


@dataclass(frozen=True)
class Problem:
    """問題 1 つの情報。

    Attributes:
        id (str): 問題 ID。
        chunks (int): この問題における分割データの個数。
        start_at (int): この問題に対して回答できるようになる時刻 (UNIX エポック)。
        time_limit (int): start_at から数え始めて、回答できる制限時間の秒数。
        data (int): 重なっている音声データの個数。含まれている音声データの番号はこの個数だけ回答しなければならない。
    """
    id: str
    chunks: int
    start_at: int
    time_limit: int
    data: int


@dataclass(frozen=True)
class Chunk:
    """1 つの分割データ。

    Attributes:
        segment_index (int): 全ての分割データの中で、この分割データが何番目に属しているのかを表す。
        wav (numpy.ndarray): 音声波形の配列。要素の型は float。
    """
    segment_index: int
    wav: np.ndarray


@dataclass(frozen=True, order=True)
class Answer:
    """問題に対する回答の情報。

    Attributes:
        problem_id (str): 回答しようとしている問題の ID。
            Requester の get_problem で取得した、Problem の id を入れることが期待される。
        answers (list[str]): 問題の断片データに含まれていると判断した読みデータ番号のリスト。
            左を 0 埋めした 2 桁の文字列を格納すること。
            この長さは、problem_id に指定した id を持つ Problem の data と同じでなければならない。
    """
    problem_id: str
    answers: list[str]


class AbstractRequester(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_match(self) -> Match:
        pass

    @abc.abstractmethod
    def get_problem(self) -> Problem:
        pass

    @abc.abstractmethod
    def get_chunks(self, using_chunks: int, save_dir: str) -> list[Chunk]:
        pass

    @abc.abstractmethod
    def post_answer(self, answer: Answer) -> None:
        pass
