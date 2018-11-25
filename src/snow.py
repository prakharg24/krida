import sys
import numpy as np
import heapq

sweden_dict = {"A":0, "B":0, "C":0, "D":0, "o":1, ".":0, "#":float("inf")}
houses_ind = ["A", "B", "C", "D"]
rev_houses = {0:"A", 1:"B", 2:"C", 3:"D"}

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
					new_case["houses"][cha] = (row_count, i)
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
	dist_mat[sti][stj] = mat[sti][stj]
	# dist_mat[sti][stj] = 0
	vis_mat = np.zeros((len(mat),len(mat[0])))
	curr_set = []
	heapq.heappush(curr_set, (mat[sti][stj], (sti, stj)))
	# heapq.heappush(curr_set, (0, (sti, stj)))
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

	fnl_mat = []
	for i in range(n):
		row = []
		for j in range(m):
			row.append({"dij" : dijkstras(ele["mat"], i, j), "subset" : np.zeros((16)), "last" : np.zeros((16, 2))})
		fnl_mat.append(row)

	houses = [1, 2, 4, 8]
	for ind, hus in enumerate(houses):
		house_c = ele["houses"][rev_houses[ind]]
		for i in range(n):
			for j in range(m):
				fnl_mat[i][j]["subset"][hus] = fnl_mat[i][j]["dij"][house_c[0]][house_c[1]]
				fnl_mat[i][j]["last"][hus][0] = i
				fnl_mat[i][j]["last"][hus][1] = j

	for sub in range(1, 16):
		if sub in houses:
			continue
		first_update = np.ones((n, m)) * float("inf")
		for subsub in range(1, sub):
			if(subsub & sub == subsub):
				sec1 = subsub
				sec2 = subsub ^ sub
				for i in range(n):
					for j in range(m):
						curr_subset = fnl_mat[i][j]["subset"]
						min_join = curr_subset[sec1] + curr_subset[sec2] - ele["mat"][i][j]
						if(min_join < first_update[i][j]):
							first_update[i][j] = min_join

		for i in range(n):
			for j in range(m):
				min_val = first_update[i][j]
				for i2 in range(n):
					for j2 in range(m):
						poss_min = first_update[i2][j2] + fnl_mat[i][j]["dij"][i2][j2] - ele["mat"][i2][j2]
						if(poss_min < min_val):
							min_val = poss_min
				fnl_mat[i][j]["subset"][sub] = min_val

	min_val = float("inf")
	for i in range(n):
		for j in range(m):
			if(fnl_mat[i][j]["subset"][15] < min_val):
				min_val = fnl_mat[i][j]["subset"][15]

	print(min_val)
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
