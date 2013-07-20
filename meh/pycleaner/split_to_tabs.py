import re

lines = open("input.txt")


def split_line(line):
    
    timestamp_index = re.search("(\d+:*)+",line).end()
    ts = line[0:timestamp_index]
    return [ts,line]

def line_array_formatter(lines):
    for ln in lines:
        ln = split_line(ln)
        print ln

line_array_formatter(lines)