import sys
import numpy as np

sweden_dict = {"A":0, "B":0, "C":0, "D":0, "o":1, ".":0, "#":float("inf")}
houses_ind = ["A", "B", "C", "D"]

def get_input(fname):
	raw_data = open(fname, "r")
	all_cases = []
	new_case = {}
	row_count = 0
	for columns in ( raw.strip().split() for raw in raw_data ):
		if(len(columns)==2):
			new_case["n"] = int(columns[0])
			new_case["m"] = int(columns[1])
			new_case["map"] = []
			new_case["mat"] = []
			new_case["houses"] = {}
		elif(len(columns)==1):
			map_row = []
			mat_row = []
			for i, cha in enumerate(columns[0]):
				map_row.append(cha)
				mat_row.append(sweden_dict[cha])
				if cha in houses_ind:
					new_case["houses"][cha] = (i, row_count)
			new_case["map"].append(map_row)
			new_case["mat"].append(mat_row)
			row_count += 1
		
		if(row_count==new_case["m"]):
			all_cases.append(new_case)
			new_case = {}
			row_count = 0

	return all_cases

inputFile = sys.argv[1]
outputFile = sys.argv[2]

inp = get_input(inputFile)

fileout = open(outputFile, "w")

for ele in inp:
	new_ele = solve(ele)
	n = new_ele["n"]
	m = new_ele["m"]
	fileout.write(str(n) + " " + str(m) + "\n")
	for i in range(n):
		for j in range(m):
			fileout.write(new_ele["map"][i][j])
		fileout.write("\n")
	fileout.write("\n")
