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


if __name__ == "__main__":
    schema = read_schema()
    load_ml()
    load_reference_data()
    with open(sys.argv[1]) as f:
        out = read_json(f)
