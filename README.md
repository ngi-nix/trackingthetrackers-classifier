# Tracking classifier

Version 0.2.0

## Overview

This repository contains the code / python scripts for taking the [JSON format definitions of feature vectors](https://gitlab.com/trackingthetrackers/wiki/-/wikis/JSON-format-definition-for-feature-vectors) for the [TTT](https://gitlab.com/trackingthetrackers/wiki) project and turns such a JSON definition 
into a result : contains trackers Y/N (possibly with probabilities)

Input on stdin:
  * A JSON dict in the format of https://gitlab.com/trackingthetrackers/wiki/-/wikis/JSON-format-definition-for-feature-vectors
  
(note: should something in the JSON format change, then you can re-create the JSON schema.json file via https://extendsclass.com/json-schema-validator.html)


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
python fe_json2csv.py tests/
```


``main.py`` will iterate over the ``tests/`` directory and look at subdirs "clean" and "trackers" and search for .json files in there.
It expects these JSON input files in the described format (see above) and produces an output of it's a tracker or not as a JSON array:
python main.py tests/in.json

```json
[
  { "file": "tests/clean/in.json", 
    "ground truth": "clean", 
    "prediction": {"trackers": 0.0, "clean": 1.0}}, 
  { "filename": "tests/trackers/1c763d1a1d94cd9a242425f515559aae52576d5e08ab069dfe82677cb15ddfba.json", 
    "ground truth": "trackers", 
    "prediction": {"trackers": 0.0, "clean": 1.0}
  }
]
```

## Integration into other workflows / tools / issuebot

  - make sure it works for you on the cmd line (see Testing above)
  - for each APK, generate the JSON file in a folder . The folder should be either "clean" or "trackers". I.e. the folder 
  name is the label.
  - for these JSON files, call the main.py script with the directory where ``clean/`` and ``trackers/`` reside in.
  See the testing example above.
  - the main.py writes onto stdout a JSON answer on how probable it thinks that something contains trackers or not.

