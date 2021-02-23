import sys
import numpy as np
import datetime

print 'first file is the pdb file and second file is the top file'

f1=open(sys.argv[1], "r")
f2=open(sys.argv[2], "r")

f2Mat = []
f1Mat = []

add = False
for line in f2:
    if 'bonds' in line:
	add = False
    if add == True:
	f2Mat.append(line.split())		
    if 'atoms' in line:
	add = True

del f2Mat[0]

for i in range(len(f2Mat)-1,-1,-1):
    if len(f2Mat[i]) <= 1:
	del f2Mat[i]

print f2Mat
print '\n\n\n\n'
print len(f2Mat)
for j in range(0,8):
    f1.readline()
for j in range(0,len(f2Mat)):
    f1Mat.append(f1.readline().split())

print f1Mat[0]
print f2Mat[0]

if len(f2Mat) != len(f1Mat):
    print 'mismatch'
    exit()

for i in range(0, len(f1Mat)):
    print "%5i%5s%5s%5i%8.3f%8.3f%8.3f" % (1,f2Mat[i][3],f2Mat[i][4],(int(i)+1),float(f1Mat[i][len(f1Mat[i])-6])/10,float(f1Mat[i][len(f1Mat[i])-5])/10,float(f1Mat[i][len(f1Mat[i])-4])/10)


fout = open("out.gro", "w")
fout.write('; Polymer interaction file generated by Maziar Fayaz Torshizi, Erich Muller on %s\n' % (datetime.date.today()))
fout.write("%i\n" % len(f1Mat))
for i in range(0, len(f1Mat)):
    fout.write("%5i%5s%5s%5i%8.3f%8.3f%8.3f\n" % (1,f2Mat[i][3],f2Mat[i][4],(int(i)+1),float(f1Mat[i][len(f1Mat[i])-6])/10,float(f1Mat[i][len(f1Mat[i])-5])/10,float(f1Mat[i][len(f1Mat[i])-4])/10))

fout.write("%10.5f%10.5f%10.5f" %(0,0,0))

fout.close()
