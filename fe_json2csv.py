#!/usr/bin/env python

"""
features extraction converter: in comes the JSON (dict) as specified by schema.json
Out goes the CSV as expected by the inference() function.
"""

import pandas as pd

def convert_fe_json2csv(j: dict) -> pd.Series:
    pass