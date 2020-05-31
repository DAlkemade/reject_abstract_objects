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
    input = pd.read_csv('dev.csv')
    y_true = list(input['abstract'])
    y_pred = list()
    for entity in tqdm.tqdm(list(input['object'])):
        res = check_abstract(entity)
        y_pred.append(res)

    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    logger.info(f'Precision: {precision}')
    logger.info(f'Recall: {recall}')


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Unhandled exception")
        raise
