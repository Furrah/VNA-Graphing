import matplotlib.pyplot as plt
import numpy as np 


def get_data_LT(file):
	with open(file,'r') as infile:	
		infile = infile.read()
		data = infile.split('\n')

		data = data[5:]

		D = [[] for i in range(9)]

		print(data[0])
		print(len(data))
		for eachline in data:

			if len(eachline) > 0:
				eachline = eachline.split('\t')



				for i in range(len(eachline)):
					D[i].append(float(eachline[i]))


		return D


file = "/Users/Joe/Desktop/OUT1.S2P"

A = get_data_LT(file)

plt.plot(A[0],A[1])
plt.show()