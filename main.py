#!/usr/bin/env python

import os
import sys
import json
from jsonschema import validate
import fileinput

schema = dict()


def load_ml():
    pass

def inference(j: str) -> dict:
    result = {"trackers": 0.99, "clean": 0.01}
    return result


def read_schema(path: str = "./schema.json"):
    global schema
    with open(path) as f:
        schema = json.load(f)
        return schema


def read_json(f):
    try:
        data = json.load(f)
    except Exception as ex:
        print("could not parse input (skipping file). Reason %s" % (str(ex),))
        return None
    # validate it
    try:
        validate(instance=data, schema=schema)
    except Exception as ex:
        print("could not validate input (skipping line). Reason %s" % (str(ex),))
        return None
    # to the inference, return the output
    return inference(data)


if __name__ == "__main__":
    schema = read_schema()
    load_ml()
    with open(sys.argv[1]) as f:
        out = read_json(f)
        print("result: %r" % out)
