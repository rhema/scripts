import re

lines = open("data/input.txt")
lines = open("data/pinterestall.txt")

q_regex = re.compile("\[(.+)\]")

all_codes = {}

def split_line(line):
    tabbed = line.split("\t")
    #print len(tabbed)
    participant = tabbed[0]
    order = tabbed[1]
    line = "".join(tabbed[2:])#maybe no..
    #get the last tree....
    codes = tabbed[-3:]
    #print "CODEMETEMBER::::",codes
    clean_codes = []
    for c in codes:
        if '[' in c or '?' in c or len(c) < 2 or len(c.split(" ")) > 1 or ":" in c:
            continue
        code = c
        clean_codes += [code.upper().strip()]
        all_codes[code.upper().strip()] = 1
        line.replace(c,code)
    #print clean_codes
    
    timestamp_index = 0
    #print "LBEFORE",line
    try:
        timestamp_index = re.search("(\d+:*)*",line).end()
    except:
        print line
        print "NO TIMESTAMP"
        print "NO TIMESTAMP"
        print "NO TIMESTAMP"
        print "NO TIMESTAMP"
        print "NO TIMESTAMP"
        print "NO TIMESTAMP"
    ts = line[0:timestamp_index]
    #assume 1 questions
    #m = re.search(r"\[([A-Za-z0-9_]+)\]", line)
    #m = re.search(r"\[(.+)\]", line)
    qs = q_regex.findall(line)
    if len(qs) == 0:
        qs = [""]
    else:
        qs = [qs[-1]]
#    try:
    #print "QUESTIONS:->",qs
#    if len(qs) > 1:
#        print "HERE IT IS!!! ",qs
#    print qs
    #print len(m)
#    except:
#        print "NO QUESTIONS"
    #detect more than one question...
    clean_line = line[timestamp_index:].rstrip()
    for i in range(0,len(qs)):
        if len(qs[i]) > 3:
            clean_line = clean_line.replace(qs[i],str(i+1))    
    ret = [participant,order,ts,clean_line,"+".join(qs)]+clean_codes
    #print len(ret),ret
    return ret

def line_array_formatter(lines):
    for ln in lines:
        ln = split_line(ln)
        print "\t".join(ln)
        #print ln[0]+"\t"+ln[1]

line_array_formatter(lines)
#zz = all_codes.keys()
#zz.sort()
#print "\t".join(zz)