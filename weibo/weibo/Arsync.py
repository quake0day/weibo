import os
import sys

command = "rsync -avl -e ssh quake0day@www.quake0day.com:"
add1 = sys.argv[1]
add2 = sys.argv[2]
direct = sys.argv[3]

command_final = command + add1 + " " + add2
print command_final
print os.popen(command_final).read()

