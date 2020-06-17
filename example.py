import logging
import os

import pandas as pd
import tqdm
from logging_setup_dla.logging import set_up_root_logger
from sklearn.metrics import precision_score, recall_score

from reject_abstract_objects.reject import check_abstract

set_up_root_logger(f'reject', os.path.join(os.getcwd(), 'logs'))

logger = logging.getLogger(__name__)

THE = True

def main():
    input = pd.read_csv('test_annotated.csv')
    input = input[input['abstract'] != -1]

    logger.info(f"Percentage abstract: {input['abstract'].mean()}")

    y_true = list(input['abstract'])
    y_pred = list()
    no_results = set()
    for entity in tqdm.tqdm(list(input['object'])):
        res, no_result = check_abstract(entity, the=THE)
        y_pred.append(res)
        if no_result:
            no_results.add(entity)

    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    logger.info(f'Precision: {precision}')
    logger.info(f'Recall: {recall}')
    logger.info(f'No results: {no_results}')

    false_negatives = set()
    false_positives = set()
    for i, object in enumerate(list(input['object'])):
        pred = y_pred[i]
        gold = y_true[i]
        if pred == 1 and gold == 0:
            false_positives.add(object)
        if pred == 0 and gold == 1:
            false_negatives.add(object)

    logger.info(f'Number of mistakes: {len(false_negatives) + len(false_positives)}')
    logger.info('\nFalse positives')
    errror_analysis(false_positives, no_results)
    logger.info('\nFalse negatives')
    errror_analysis(false_negatives, no_results)


def errror_analysis(errors: set, no_results: set):
    logger.info(f'Errors (n={len(errors)}): {errors}')
    errors_no_results = errors.intersection(no_results)
    logger.info(f'Intersection errors and no_results (n={len(errors_no_results)}): {errors_no_results}')
    errors_with_results = errors - no_results
    logger.info(f'Errors - no_results (n={len(errors_with_results)}): {errors_with_results}')


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Unhandled exception")
        raise
