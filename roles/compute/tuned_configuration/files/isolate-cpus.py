import subprocess
from subprocess import call
import sys

isolcpulist = open(sys.argv[2])
line = isolcpulist.readline()
fields = line.strip().split(",")
for i in fields:
	subprocess.call(["tuna", "--cpus=" + line, sys.argv[1]])
