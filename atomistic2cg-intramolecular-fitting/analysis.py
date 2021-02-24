from matplotlib import pyplot as plt
import numpy as np

def distance(vec1, vec2):
    dist = 0
    for i in range(0, len(vec1)):
	dist = (vec1[i] - vec2[i])**2 + dist
    return dist**.5

def angle(a,b,c):
    vec1 = np.array(a)-np.array(b)
    vec2 = np.array(c)-np.array(b)
    return np.degrees(np.arccos(np.dot(vec1, vec2)/np.linalg.norm(vec1)/np.linalg.norm(vec2)))

class particle():
    def __init__(self, index, posit):
	self.index = index
	self.posit = posit

class posit():
    def __init__(self, array, plist):

	self.total = len(array)

	self.index = np.copy(array)
	self.index = self.index.tolist()
	for i in range(0, len(array)):
	    self.index[i] = particle(i+1, array[i])

	self.plist = np.copy(plist)
	self.plist = self.plist.tolist()
	for i in range(0, len(plist)):
	    for j in range(0, len(plist[i])):
		for k in range(0, len(self.index)):
		    if plist[i][j] == self.index[k].index:
			self.plist[i][j] = self.index[k]

	    
class timing():
    def __init__(self, time, array, plist):
	self.time = time
	self.posit = posit(array,plist)


def bondDist(objArr):
    bondArr = []
    types = ['rrr', 'rsr', 'rrs']
    for i in range(0, len(objArr)-1):
	if distance(objArr[i].posit, objArr[i+1].posit) < 1:
	    bondArr.append(distance(objArr[i].posit, objArr[i+1].posit))
    return bondArr

def angDist(objArr):
    #print 'angDist'
    #print 'Length of input is'
    #print len(objArr)
    angArr = []
    types = ['rrr', 'rsr', 'rrs']
    for i in range(0, len(objArr)-2):
	if distance(objArr[i].posit, objArr[i+1].posit) < 2 and distance(objArr[i+1].posit, objArr[i+2].posit) < 2:
	    angArr.append(angle(objArr[i].posit, objArr[i+1].posit, objArr[i+2].posit))
    return angArr






##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################

numframes 	= 300
numMono 	= 6
numPoly 	= 50
bonds 		= True
bonds 		= False


polyList = []
polymer = []
for i in range(0, numMono*numPoly):
    polymer.append(i+1)
    if (i+1) % numMono == 0:
	polyList.append(polymer)
        polymer = []

print 'starting to read the files'
time = []
for i in range(0, numframes):
    print i
    t = i

    f = open("%i.gro" %i, "r")
    f.readline()
    f.readline()
   
    positArr = []
    for j in range(0, numMono*numPoly):
   	words = f.readline().split()
	positArr.append([float(words[len(words)-3]), float(words[len(words)-2]), float(words[len(words)-1])])

    time.append(posit(positArr, polyList))


print 'calculating distributions'
distancez = []
for i in range(0, len(time)):
#for i in range(0, numframes):
    if i % len(time)/10 == 0:
	print '%i percent of distributions calculated' % int(float(i)/len(time))
    if bonds == True:
        for j in range(0, len(time[i].plist)):
            kuala = bondDist(time[i].plist[j])
            for k in range(0, len(kuala)):
                distancez.append(kuala[k])
    else:
        for j in range(0, len(time[i].plist)):
            kuala = angDist(time[i].plist[j])
            for k in range(0, len(kuala)):
                distancez.append(kuala[k])

if bonds == True:
    bw = 0.005
    np.savetxt("bonds/distancez.xvg", distancez)
    fig = plt.figure()
    plt.hist(distancez, bins=np.arange(min(distancez), max(distancez) + bw, bw), normed = True)

    histz = np.histogram(distancez, bins=np.arange(min(distancez), max(distancez) + bw, bw), normed = True)

    histF = []
    for i in range(0, len(histz[0])):
	histF.append([histz[1][i], histz[0][i]])

     
else:
    bw = 1
    np.savetxt("angles/distancez.xvg", distancez)
    fig = plt.figure()
    #plt.hist(distancez, bins=np.arange(min(distancez), max(distancez) + bw, bw), normed = True)

    histz = np.histogram(distancez, bins=np.arange(min(distancez), max(distancez) + bw, bw), normed = True)

    histF = []
    for i in range(0, len(histz[0])):
	histF.append([histz[1][i], histz[0][i]])


histF = np.array(histF)
np.savetxt('hist.xvg', histF)
plt.plot(histF[:,0], histF[:,1])
plt.ylabel('probability (unnormalised with respect to sin(theta))')
plt.xlabel('angle / degrees')
plt.savefig('temp.png')
plt.show()

