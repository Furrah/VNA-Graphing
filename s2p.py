import matplotlib.pyplot as plt
import numpy as np 
import os 

def get_data_LT(file):
	with open(file,'r') as infile:	
		infile = infile.read()
		data = infile.split('\n')

		data = data[5:]

		D = [[] for i in range(9)]

		# print(data[0])
		# print(len(data))
		for eachline in data:

			if len(eachline) > 0:
				eachline = eachline.split('\t')



				for i in range(len(eachline)):
					D[i].append(float(eachline[i]))


		return D


file = "/Users/Joe/Desktop/OUT1.S2P"

A = get_data_LT(file)

cut_off = 0


initial_gain = A[3][0]

print(initial_gain)

for i,value in enumerate(A[3]):

	# print(value)
	if ( value+initial_gain)  < -3:
		cut_off = i

		break

# print(cut_off)
print(abs(initial_gain) + abs(A[3][cut_off])) 

print(A[3][cut_off])
print(A[3][0] - A[3][cut_off])
print(A[0][cut_off]/1e6)



print(os.path.basename(file))
 

plt.plot(A[0],A[3])
plt.show()