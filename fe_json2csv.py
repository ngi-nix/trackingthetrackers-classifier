#!/usr/bin/env python

"""
features extraction converter: in comes the JSON (dict) as specified by schema.json
Out goes the CSV as expected by the inference() function.
"""

import pandas as pd
import sys
import json

all_domains = pd.Series()
all_perms = pd.Series()


def load_domains(path: str):
    global all_domains

    try:
        all_domains = pd.read_csv(path, header=None, squeeze=True)
    except Exception as ex:
        print("could not load the domains list (faup hosts). Reason %s" % str(ex))
        sys.exit(255)
    return all_domains


def load_perms(path: str):
    global all_perms

    try:
        all_perms = pd.read_csv(path, header=None, squeeze=True)
    except Exception as ex:
        print("could not load the permission list (list of all possible perms). Reason %s" % str(ex))
        sys.exit(254)
    return all_perms


def load_reference_data():
    load_domains("reference_data/all-faup-hosts.csv")
    load_perms("reference_data/all-permissions-from-fdroid-repos.csv")


def convert_fe_json2csv(j: dict) -> pd.Series:
    """Convert a feature extraction JSON to the CSV format (pd.Series) which the inference part expects.
    :param j:  dict .. as specified in the schema.json format
    :returns:  pandas Series of the (sparse) list of matches of domains and

    """
    ver = j['meta']['ver']
    if ver != "0.2.0":
        raise Exception("error: I can only parse the JSON feature extraction format version 0.1.0")

    # first create the permissions series which we need in the inference part
    perms = set(j['apks'][0]['usesPermissions'])
    # result vector: 0/1 value in the vector component. Vector has the len of all_perms
    found_perms = []
    for p in all_perms.values:
        if p in perms:
            found_perms.append(1)
        else:
            found_perms.append(0)
    s1 = pd.Series(found_perms, index=all_perms)
    # next create the series of domains
    domains = set(j['apks'][0]['domainNames'])
    found_domains = []
    for d in all_domains.values:
        if d in domains:
            found_domains.append(1)
        else:
            found_domains.append(0)
    s2 = pd.Series(found_domains, index=all_domains)
    s3 = s1.append(s2)
    return s3


if __name__ == "__main__":
    load_reference_data()
    print("ALL DOMAINS:\n%r" % all_domains)
    print()
    print("ALL PERMS:\n%r" % all_perms)
    print()
    print(80*"=")
    infile = "tests/in.json"
    print()
    print("Trying to read the JSON file %s" % infile)
    print(80*"=")
    with open(infile) as f:
        data = json.load(f)
        print("%r" % data)
        df = convert_fe_json2csv(data)
        df.to_csv('foo.csv', header=False)
