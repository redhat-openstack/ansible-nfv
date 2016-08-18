#!/usr/bin/python
import sys

tisolated = sys.argv[1]
icpus = ""

commaitems = tisolated.split(",")
for i in commaitems:
        if i.__contains__("-"):
                (str,end) = i.split("-")
                (str,end) = (int (str), int (end))
                while (str <= end):
                        icpus = icpus + "%s" % (str) + ","
                        str = str+1
        else:
                icpus = icpus + i + ","

icpus = icpus[0:-1]
print icpus

