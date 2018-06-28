import os,time
# import subprocess
from subprocess import *

cmd = 'atprogram -t avrispmk2 -i isp -d ATtiny13A verify -fl -f eKo.hex'
p = Popen(cmd, shell = True, stdout = PIPE, stderr=PIPE)
out, err = p.communicate()
print out+err
# print err, type(err) 
# cmd = 'FlashUtilCL VerifyUSB C:\Users\sy\Desktop\silicon_production_program\efm8.hex "" 1'
# cmd = "dir"
# popen = os.popen(cmd)
# print popen
# text = popen.read()
# print "the text is ", text ,type(text)

# p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
# out, err = p.communicate()
# for line in out.splitlines():
#     print line
