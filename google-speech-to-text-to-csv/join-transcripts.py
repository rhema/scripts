"""
Usage:
    join-transcripts.py <file>...

Generates a CSV from JSON from google's speech-to-text json output files.
"""

import argparse
import json
import glob
import datetime
import csv

raws = glob.glob("raw/*json")

csvOut = csv.DictWriter(open("all-transcripts.csv","w"),fieldnames="participant startTime endTime transcript confidence channelTag".split())
# rows = []

csvOut.writeheader()

def dict_maker(line,participant):
    keeps = "transcript confidence".split()
    ret = {}
    alts = line['alternatives']
    words = alts[0]["words"]
    ret['participant'] = participant
    ret["startTime"] = words[0]["startTime"].split('s')[0]
    ret["endTime"] = line["resultEndTime"].split('s')[0]
    ret["startTime"] = str(datetime.timedelta(seconds=float(ret["startTime"])))
    ret["endTime"] = str(datetime.timedelta(seconds=float(ret["endTime"])))
    ret["channelTag"] = 0
    if "channelTag" in line:
        ret["channelTag"] = int(line["channelTag"])
    # print(line.keys())
    for k in keeps:
        ret[k] = alts[0][k]
    # print(words)#words has some more in
    return ret

def main(files):
    for f in files:
        print(f)
        participant = f#.split("-")[0].split(".")[0].split('/')[1]
        parsed = json.load(open(f))
        for line in parsed["results"]:
            row = dict_maker(line,participant)
            csvOut.writerow(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    opts = parser.parse_args()
    print(opts.files)
    main(opts.files)