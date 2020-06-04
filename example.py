import logging
import os

import pandas as pd
import tqdm
from logging_setup_dla.logging import set_up_root_logger
from sklearn.metrics import precision_score, recall_score

from reject_abstract_objects.reject import check_abstract

set_up_root_logger(f'reject', os.path.join(os.getcwd(), 'logs'))

logger = logging.getLogger(__name__)


def main():
    input = pd.read_csv('test_annotated.csv')
    input = input[input['abstract'] != -1]
    y_true = list(input['abstract'])
    y_pred = list()
    for entity in tqdm.tqdm(list(input['object'])):
        res = check_abstract(entity)
        y_pred.append(res)

    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    logger.info(f'Precision: {precision}')
    logger.info(f'Recall: {recall}')

    false_negatives = []
    false_positives = []
    for i, object in enumerate(list(input['object'])):
        pred = y_pred[i]
        gold = y_true[i]
        if pred == 1 and gold == 0:
            false_positives.append(object)
        if pred == 0 and gold == 1:
            false_negatives.append(object)
    logger.info(f'Number of mistakes: {len(false_negatives) + len(false_positives)}')
    logger.info(f'False positives: {false_positives}')
    logger.info(f'False negatives: {false_negatives}')


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Unhandled exception")
        raise
