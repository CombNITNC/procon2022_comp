from math import ceil
from typing import Optional
from solver.card import CardIndex, \
    ShouldPickCardsByProblem, \
    should_pick_cards_from_yaml
from solver.const import ScoreConstant
from solver.pick_ways import solve_by_binary_search
from solver.request import Answer, Requester
from ml.maesyori import preprocess_input
from os import getenv
from os.path import join, exists
from dotenv import load_dotenv
import tensorflow as tf
import numpy as np
from numpy import ndarray

from solver.score import calc_score
from solver.state import SolverState, solver_state_from_yaml

load_dotenv()

TEMP_YAML_DIR = getenv('TEMP_YAML_DIR')
MODEL_PATH = getenv('MODEL_PATH')
ENDPOINT = getenv('ENDPOINT')
TOKEN = getenv('TOKEN')

if TEMP_YAML_DIR is None or TEMP_YAML_DIR == '':
    raise Exception('env `TEMP_YAML_DIR` was not set')
if MODEL_PATH is None or MODEL_PATH == '':
    raise Exception('env `MODEL_PATH` was not set')
if ENDPOINT is None or ENDPOINT == '':
    raise Exception('env `ENDPOINT` was not set')
if TOKEN is None or TOKEN == '':
    raise Exception('env `TOKEN` was not set')

PICK_CARDS_YAML = join(TEMP_YAML_DIR, 'pick-cards.yaml')
STATE_YAML = join(TEMP_YAML_DIR, 'solver-state.yaml')


def main():
    print(f'Using temp path: {TEMP_YAML_DIR}')
    print(f'Using model path: {MODEL_PATH}')
    print(f'Accessing endpoint: {ENDPOINT}')

    model: Optional[tf.keras.Model] = tf.keras.models.load_model(MODEL_PATH)

    if model is None:
        raise Exception(f'model was not found at {MODEL_PATH}')

    req = Requester(endpoint=ENDPOINT, token=TOKEN)
    match = req.get_match()
    score_const = ScoreConstant(1, match.bonus_factor, match.penalty)

    print(match)

    should = should_pick_cards_from_yaml(PICK_CARDS_YAML) \
        if exists(PICK_CARDS_YAML) \
        else ShouldPickCardsByProblem()
    current_state = solver_state_from_yaml(STATE_YAML) \
        if exists(STATE_YAML) \
        else SolverState(
        current_problem_id='',
        used_chunks=[],
    )

    while True:
        problem = req.get_problem()
        current_state.current_problem_id = problem.id
        score_max = 0
        answers: list[Answer] = []

        for using_chunks in range(1, problem.chunks + 1):
            chunks = req.get_chunks(using_chunks, TEMP_YAML_DIR)

            images = []
            for chunk in chunks:
                image = preprocess_input(chunk.wav)
                images.append(image)
            prediction: ndarray = model.predict(np.array(images))
            prediction_avg = np.average(prediction, axis=0)

            probabilities: list[float] = prediction_avg.tolist()
            print("probabilities: ", probabilities)
            for index in range(0, len(probabilities)):
                should.insert(
                    current_state.current_problem_id,
                    CardIndex(index + 1), probabilities[index]
                )
            should.set_picks_on(current_state.current_problem_id, problem.data)

            solution = solve_by_binary_search(match.problems, should)
            if solution is not None:
                picks_by_problem, acc = solution
                corrects = ceil(problem.data * acc)
                fails = ceil(problem.data * (1 - acc))
                score = calc_score(
                    corrects,
                    fails,
                    using_chunks,
                    const=score_const
                )
                if score_max < score:
                    score_max = score
                    for picks in picks_by_problem:
                        answers.append(Answer(
                            problem_id=problem.id,
                            answers=list(map(
                                lambda card_index: card_index.as_0_pad(),
                                picks,
                            ))
                        ))

                should.save_yaml(TEMP_YAML_DIR)
                current_state.save_yaml(STATE_YAML)
                break

            print(f'solution not found with using {using_chunks} chunks')

        for answer in answers:
            req.post_answer(answer)


if __name__ == '__main__':
    main()