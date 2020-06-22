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


## Testing

