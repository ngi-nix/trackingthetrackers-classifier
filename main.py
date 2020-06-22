#!/usr/bin/env python

import os
import sys
import json
from jsonschema import validate
import fileinput

schema = dict()


def read_schema(path: str = "./schema.json"):
    global schema
    with open(path) as f:
        schema = json.load(f)
        return schema


def read_json(j: str):
    try:
        data = json.loads(j)
    except Exception as ex:
        print("could not parse input (skipping line). Reason %s" % (str(ex),))
        return None
    # validate it
    try:
        validate(instance=data, schema=schema)
    except Exception as ex:
        print("could not validate input (skipping line). Reason %s" % (str(ex),))
        return None
    # to the inference, return the output
    result = {"trackers": 0.99, "clean": 0.01}
    return result


if __name__ == "__main__":
    schema = read_schema()
    read_json(fileinput.input())
