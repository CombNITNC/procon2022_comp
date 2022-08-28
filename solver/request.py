from dataclasses import dataclass

import numpy as np
import requests
from scipy.io import wavfile


@dataclass(frozen=True)
class Match:
    problems: int
    bonus_factor: list[float]
    penalty: int


@dataclass(frozen=True)
class Problem:
    id: str
    chunks: int
    starts_at: int
    time_limit: int
    data: int


@dataclass(frozen=True)
class Chunk:
    segment_index: int
    wav: np.ndarray


@dataclass(frozen=True)
class Answer:
    problem_id: str
    answers: list[str]


@dataclass(frozen=True)
class Requester:
    endpoint: str
    token: str

    def __headers(self) -> dict[str, str]:
        return {
            "procon-token": self.token
        }

    def get_match(self) -> Match:
        res = requests.get(f"{self.endpoint}/match", headers=self.__headers())
        if not res.ok:
            raise Exception(res.text)
        return Match(**res.json())

    def get_problem(self) -> Problem:
        res = requests.get(
            f"{self.endpoint}/problem",
            headers=self.__headers()
        )
        if not res.ok:
            raise Exception(res.text)
        return Problem(**res.json())

    def get_chunks(self, using_chunks: int) -> list[Chunk]:
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
