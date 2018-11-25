import sys
import numpy as np
import heapq

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

def check_edge(mat, i, j, diri, dirj):
	newi = i + diri
	newj = j + dirj
	if(newi < 0 or newi >= len(mat)):
		return False
	if(newj < 0 or newj >= len(mat)):
		return False

	return True

def dijkstras(mat, sti, stj):
	dist_mat = np.ones((len(mat),len(mat[0]))) * float("inf")
	dist_mat[sti][stj] = 0
	vis_mat = np.zeros((len(mat),len(mat[0])))
	curr_set = []
	heapq.heappush(curr_set, (0, (sti, stj)))
	while(len(curr_set)!=0):
		curr_ele = heapq.heappop(curr_set)
		curr_dis = curr_ele[0]
		curr_x = curr_ele[1][0]
		curr_y = curr_ele[1][1]
		if(vis_mat[curr_x][curr_y]==1):
			continue
		for i in [-1, 1]:
			if(check_edge(mat, curr_x, curr_y, i, 0) and vis_mat[curr_x+i][curr_y]==0):
				min_dist = curr_dis + mat[curr_x+i][curr_y]
				if(dist_mat[curr_x+i][curr_y] > min_dist):
					dist_mat[curr_x+i][curr_y] = min_dist
					heapq.heappush(curr_set, (min_dist, (curr_x+i, curr_y)))
			if(check_edge(mat, curr_x, curr_y, 0, i) and vis_mat[curr_x][curr_y+i]==0):
				min_dist = curr_dis + mat[curr_x][curr_y+i]
				if(dist_mat[curr_x][curr_y+i] > min_dist):
					dist_mat[curr_x][curr_y+i] = min_dist
					heapq.heappush(curr_set, (min_dist, (curr_x, curr_y+i)))
		vis_mat[curr_x][curr_y] = 1

	return dist_mat


def solve(ele):
	n = ele["n"]
	m = ele["m"]
	
	new_mat = dijkstras(ele["mat"], 0, 0)
	print(new_mat)
	return ele

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
