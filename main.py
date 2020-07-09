#!/usr/bin/env python


import os
import sys
import json
from jsonschema import validate
import time
from fastai2.tabular.all import *
import pandas as pd

from fe_json2csv import load_reference_data, convert_fe_json2csv


schema = dict()
LEARN = None
CATEGORIES = None

MODEL = Path("Model/models/latest.pkl")


def load_ml():
    global LEARN
    global CATEGORIES

    t0 = time.time()
    LEARN = load_learner(MODEL)
    CATEGORIES = LEARN.dls.vocab  # classes in order of output neurons
    t1 = time.time()
    print("duration(load model): %f [sec]" % (t1 - t0), file=sys.stderr)
    return LEARN


def inference(features) -> dict:
    t0 = time.time()
    _, _, probabilities = LEARN.predict(features)
    result = {'trackers': probabilities[1].item(), 'clean': probabilities[0].item()}
    # result = {"trackers": 0.99, "clean": 0.01}
    t1 = time.time()
    print("duration(inference): %f [sec]" % (t1 - t0), file=sys.stderr)
    return result


def convert_to_vec(data: dict) -> pd.Series:
    # return data
    df = convert_fe_json2csv(data)
    return df


def read_schema(path: str = "./schema.json"):
    global schema
    with open(path) as f:
        schema = json.load(f)
        return schema


def read_json(f):
    try:
        data = json.load(f)
    except Exception as ex:
        print("could not parse input (skipping file). Reason %s" % (str(ex),), file=sys.stderr)
        return None
    # validate it
    try:
        validate(instance=data, schema=schema)
    except Exception as ex:
        print("could not validate input (skipping line). Reason %s" % (str(ex),), file=sys.stderr)
        return None
    # do the inference, return the output
    return inference(convert_to_vec(data))


def evaluate_dir(basedir: Path) -> str:
    """
    walks over @basedir and expects two subfolders: clean/ and trackers/.
    In each of these, it will search for .json files and iterate over them, do the inference and
    add the result to a pd.Series which is returned.
    Return format of the pd.Series:
      * filename (hash) of the apk
      * expected result (dir was "clean" or "trackers")
      * result of the prediction
    :param basedir:
    :return: pd.Series
    """
    l = []

    files = sorted(Path(basedir).glob('**/*.json'))
    cleanfiles = filter(lambda i: "clean" in str(i), files)
    trackerfiles = filter(lambda i: "trackers" in str(i), files)
    for f in cleanfiles:
        prediction=read_json(f)
        filename = str(f)
        l.append({ "filename": filename, "ground truth": "clean", "prediction": prediction})
    for f in trackerfiles:
        prediction=read_json(f)
        filename = str(f)
        l.append({ "filename": filename, "ground truth": "trackers", "prediction": prediction})
    return json.dumps(l)
    # res = pd.Series(l)
    # res.to_csv("out.csv")

if __name__ == "__main__":
    schema = read_schema()
    load_ml()
    load_reference_data()
    print(evaluate_dir(sys.argv[1]))
