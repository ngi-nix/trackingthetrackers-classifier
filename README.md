# Tracking classifier

Version 0.1

## Overview

This repository contains the code / python scripts for taking the [JSON format defintions of feature vectors](https://gitlab.com/trackingthetrackers/wiki/-/wikis/JSON-format-definition-for-feature-vectors) for the [TTT](https://gitlab.com/trackingthetrackers/wiki) project and turns such a JSON definition 
into a result : contains trackers Y/N (possibly with probabilities)

Input on stdin:
  * A JSON dict in the format of https://gitlab.com/trackingthetrackers/wiki/-/wikis/JSON-format-definition-for-feature-vectors
  
Output on stdout: 
  * JSON dict: { "trackers": 0.976, "clean": 0.024 }
 
## Installation


```bash
git clone https://gitlab.com/trackingthetrackers/classifier
# (...make a virtual env and source it, or use conda or pip as you like. Example....)
source venv/bin/activate
pip install -r requirements.txt
```

## Testing

```bash
# test if the feature extractor JSON to csv converter works:
python fe_json2csv.py tests/in.json

# test the main script. This expects a JSON input file of features (see above) and produces an output of it's a tracker or not:
python main.py tests/in.json

```
