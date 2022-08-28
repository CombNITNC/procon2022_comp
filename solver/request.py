from dataclasses import dataclass

import numpy as np
import requests
from scipy.io import wavfile


@dataclass(frozen=True)
class Match:
    """試合全体を通して変化しない、問題全体で共通の情報。

    試合全体を通して、同じ取り札は日本語か英語かに関わず 1 度までしか登場しない。例えば、E01 がすでに読み上げられた場合は J01 は登場しない。

    Attributes:
        problems (int): 試合中の問題数。
        bonus_factor (list[float]): スコア計算のボーナス係数のリスト。
            使用した分割数 n 個に対して n 番目の係数が適用される。
        penalty (int): 変更札である取り札のスコアに対して適用される係数。
    """
    problems: int
    bonus_factor: list[float]
    penalty: int


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
    starts_at: int
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


@dataclass(frozen=True)
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


@dataclass(frozen=True)
class Requester:
    """問題 API に対してリクエストを送るためのクラス。

    Parameters:
        endpoint (str): API のエンドポイントの URL。
        token (str): API のエンドポイントで認証するためのトークン。
    """
    endpoint: str
    token: str

    def __headers(self) -> dict[str, str]:
        return {
            "procon-token": self.token
        }

    def get_match(self) -> Match:
        """試合全体を通して変化しない、問題全体で共通の情報を取得する。

        Raises:
            InvalidToken: トークンが不正
            AccessTimeError: 試合時間外のリクエスト

        Returns:
            Match: 試合の情報。
        """
        res = requests.get(f"{self.endpoint}/match", headers=self.__headers())
        if not res.ok:
            raise Exception(res.text)
        return Match(**res.json())

    def get_problem(self) -> Problem:
        """現在出題中の問題の情報を取得する。

        Raises:
            InvalidToken: トークンが不正
            AccessTimeError: 回答時間外のリクエスト

        Returns:
            Problem: 問題の情報。
        """
        res = requests.get(
            f"{self.endpoint}/problem",
            headers=self.__headers()
        )
        if not res.ok:
            raise Exception(res.text)
        return Problem(**res.json())

    def get_chunks(self, using_chunks: int) -> list[Chunk]:
        """現在出題中の問題における断片データのリストを取得する。

        Args:
            using_chunks (int): 使用する断片データの個数。使用した断片データの個数は記録されるため、少ない数から試すこと。

        Raises:
            InvalidToken: トークンが不正
            AccessTimeError: 回答時間外のリクエスト
            FormatError: Problem の chunks の値よりも大きい数が指定されたなど、不正な入力データ

        Returns:
            list[Chunk]: 断片データのリスト。長さは using_chunks に等しいことが期待される。
        """
        chunks_res = requests.post(
            f"{self.endpoint}/problem/chunks",
            headers=self.__headers(),
            params={"n": using_chunks}
        )
        if not chunks_res.ok:
            raise Exception(chunks_res.text)
        chunks: list[Chunk] = []
        for chunk_filename in chunks_res.json()["chunks"]:
            index = int(chunk_filename.split("_")[0][7:])
            file_res = requests.get(
                f"{self.endpoint}/problem/chunks/{chunk_filename}",
                headers=self.__headers(),
                stream=True
            )
            if not file_res.ok:
                raise Exception(file_res.text)
            wav = wavfile.read(file_res.raw)
            chunks.append(Chunk(segment_index=index, wav=wav))
        return chunks

    def post_answer(self, answer: Answer) -> None:
        """指定の問題に対して回答する。出題中の問題よりも過去の問題に対して、回答を再提出することもできる。

        Args:
            answer (Answer): 回答する内容。

        Raises:
            InvalidToken: トークンが不正
            AccessTimeError: 指定の問題に対して回答時間外のリクエスト
            TooLargeRequestError: 送信内容の JSON の本文が 1024 バイトを超えた
            FormatError: 無効な問題 ID など、入力形式が不正
        """
        headers = {
            "Content-Type": "application/json"
        }
        headers.update(self.__headers())
        res = requests.post(
            f"{self.endpoint}/problem",
            headers=headers,
            data={
                "problem_id": answer.problem_id,
                "answers": answer.answers
            }
        )
        if not res.ok:
            raise Exception(res.text)
        print(res.text)
