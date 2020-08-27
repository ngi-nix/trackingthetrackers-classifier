#! /bin/env python

"""
Calculate various statistical parameters (confusion matrix, precision, accuracy, recall, ...).
Expects a json file in the following format (example):

[ { "filename": "tests/clean/in.json",
    "ground truth": "clean",
    "prediction": { "trackers": 0, "clean": 1 }
  },
  { "filename": "tests/trackers/1c763d1a1d94cd9a242425f515559aae52576d5e08ab069dfe82677cb15ddfba.json",
    "ground truth": "trackers",
    "prediction": { "trackers": 0, "clean": 1 }
  }
]


versions used:
Python             3.8.3
"""

import sys
import json
from tabulate import tabulate
from typing import Dict
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

if len(sys.argv) != 2:
    raise TypeError(f"this script takes exactly 1 parameter (a json file), got: {sys.argv}")

INPUT_JSON = sys.argv[1]
LABELS = ["clean", "trackers"]

# reading json
with open(INPUT_JSON, "r") as in_file:
    data = json.load(in_file)

y_true = []
y_pred = []

for apk in data:  # type: Dict
    y_true.append(apk["ground truth"])
    if apk["prediction"]["clean"] == 1:
        y_pred.append("clean")
    else:
        y_pred.append("trackers")


class SizeMismatchError(Exception):
    pass


class LabelMismatchError(Exception):
    pass


# sanity checks
if len(y_true) != len(y_pred):
    raise SizeMismatchError(f"there should be one prediction for every ground truth, instead got size ground truth: {len(y_true)}, size predictions: {len(y_pred)}")

found_keys = sorted(data[0]["prediction"].keys())
if found_keys != LABELS:
    raise LabelMismatchError(f"expected {LABELS}, got {found_keys}")

# calculating confusion matrix
cmatrix = confusion_matrix(y_true=y_true, y_pred=y_pred, labels=LABELS)

accuracy = accuracy_score(y_true=y_true, y_pred=y_pred)
precision = precision_score(y_true=y_true, y_pred=y_pred, average=None, labels=LABELS)
recall = recall_score(y_true=y_true, y_pred=y_pred, average=None, labels=LABELS)
f1 = f1_score(y_true=y_true, y_pred=y_pred, average=None, labels=LABELS)

if __name__ == "__main__":
    cm = []
    cm.append([LABELS[0]] + cmatrix[0].tolist())
    cm.append([LABELS[1]] + cmatrix[1].tolist())

    # sys.exit()
    print("# confusion matrix")
    print(tabulate(cm, headers=[""] + LABELS, tablefmt="github"))
    print()

    print("# accuracy")
    print(accuracy)

    print()
    print("# precision")
    print(tabulate([precision], headers=LABELS, tablefmt="github"))
    print()

    print("# recall")
    print(tabulate([recall], headers=LABELS, tablefmt="github"))
    print()
