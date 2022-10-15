from dataclasses import dataclass
from os.path import join
import requests
from scipy.io import wavfile

from solver.request.meta import AbstractRequester, Answer, Chunk, \
    Match, Problem


@dataclass(frozen=True)
class NetRequester(AbstractRequester):
    """問題 API に対してリクエストを送るためのクラス。

    Parameters:
        endpoint (str): API のエンドポイントの URL。
        token (str): API のエンドポイントで認証するためのトークン。
    """
    endpoint: str
    token: str

    def __headers(self) -> dict[str, str]:
        return {
            'procon-token': self.token
        }

    def get_match(self) -> Match:
        """試合全体を通して変化しない、問題全体で共通の情報を取得する。

        Raises:
            InvalidToken: トークンが不正
            AccessTimeError: 試合時間外のリクエスト

        Returns:
            Match: 試合の情報。
        """
        res = requests.get(f'{self.endpoint}/match', headers=self.__headers())
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
            f'{self.endpoint}/problem',
            headers=self.__headers()
        )
        if not res.ok:
            raise Exception(res.text)
        return Problem(**res.json())

    def get_chunks(self, using_chunks: int, save_dir: str) -> list[Chunk]:
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
            f'{self.endpoint}/problem/chunks',
            headers=self.__headers(),
            params={'n': using_chunks}
        )
        if not chunks_res.ok:
            raise Exception(f"{chunks_res.status_code} {chunks_res.text}")
        chunks: list[Chunk] = []
        for chunk_filename in chunks_res.json()['chunks']:
            index = int(chunk_filename.split("_")[0][7:])
            file_res = requests.get(
                f'{self.endpoint}/problem/chunks/{chunk_filename}',
                headers=self.__headers(),
                stream=True
            )
            if not file_res.ok:
                raise Exception(file_res.text)

            wav_path = join(save_dir, chunk_filename)
            with open(wav_path, 'wb') as f:
                f.truncate()
                f.write(file_res.content)

            _rate, wav = wavfile.read(wav_path)
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
            'Content-Type': 'application/json'
        }
        headers.update(self.__headers())
        res = requests.post(
            f'{self.endpoint}/problem',
            headers=headers,
            data={
                'problem_id': answer.problem_id,
                'answers': answer.answers
            }
        )
        if not res.ok:
            raise Exception(res.text)
        print(res.text)
