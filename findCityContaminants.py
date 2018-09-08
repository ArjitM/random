from __future__ import division

from extract_data import *
import numpy
from multiprocessing import Pool


def find(lines):
	#output, lines = junk
	output = []
	i = 0
	for line in lines:

		if i==0:
			i+=1
			continue
		i+=1

		if i == 100:
			break

		info = line.split(",")
		cityName = info[0][1:-1]
		stateID = info[2][1:-1]


		#print(info[6])
		lat = float(info[6][1:-1])
		lng = float(info[7][1:-1])

		try:
			city = getCityData(cityName, stateID)
		except:
			continue

		relative_ppbs = {c.name: c.relativePPB() for c in city.getContaminants()}
		rpvs = list(relative_ppbs.values())
		if rpvs == []:
			continue
		score_raw = numpy.mean(rpvs)
		output.append("%s, %s, %f, %s" % (cityName, stateID, score_raw, relative_ppbs))
		#print(output[-1])
	return output


cities = open('cityBase.csv', 'r') 

# outputs = []
# outputs.append(open('cityContaminants1.csv', 'w'))
# outputs.append(open('cityContaminants2.csv', 'w'))
# outputs.append(open('cityContaminants3.csv', 'w'))
# outputs.append(open('cityContaminants4.csv', 'w'))
# outputs.append(open('cityContaminants5.csv', 'w'))

lines = cities.readlines()
# k = len(lines) // 5

# lines_p = []

# lines_p.append(lines[0:k])
# lines_p.append(lines[k:k*2])
# lines_p.append(lines[k*2:k*3])
# lines_p.append(lines[k*3:k*4])
# lines_p.append(lines[k*4:])

# p = Pool(5)
# data = p.map(find, lines_p)
data = find(lines)
output = open('cityContaminants.csv', 'w')
for d in data:
	output.write(d + '\n')

output.close()

cities.close()






