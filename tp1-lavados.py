def load_file(file):
	map_clothes = {}
	lis_clothes_weight = []
	with open(file, 'r', encoding='utf-8') as file:
		for line in file:
			lis_line = line.split()
			if line.startswith("p"):
				lenght_clothes = lis_line[2]
				lenght_incompatibilty = lis_line[3]
			elif line.startswith("e"):
				first_clothes = lis_line[1]
				second_clothes = lis_line[2]
				if first_clothes not in map_clothes:
					map_clothes[first_clothes] = {}
				map_clothes[first_clothes][second_clothes] = True
				if second_clothes not in map_clothes:
					map_clothes[second_clothes] = {}
				map_clothes[second_clothes][first_clothes] = True
			elif line.startswith("n"):
				clothes = lis_line[1]
				weight = int(lis_line[2])
				lis_clothes_weight.append((clothes, weight))
	return map_clothes, lis_clothes_weight

def is_compatible(map_clothes, a_clothes, another_clothes):
	return another_clothes not in map_clothes[a_clothes]

def is_compatible_set_wash(set_wash, map_clothes, another_clothes):
	compatible = True
	for clothes, weight in set_wash:
		compatible &= is_compatible(map_clothes, clothes, another_clothes)
	return compatible


def build_lavados(file_name):
	map_clothes, lis_clothes_weight = load_file(file_name)
	#lis_clothes_weight_sort = sorted(lis_clothes_weight, key=lambda tup: tup[1], reverse=False)

	washeds = []

	for clothes_1, weight_1 in lis_clothes_weight:
		lis_clothes_weight_clone = lis_clothes_weight.copy()
		set_clothes = { (clothes_1, weight_1) }
		for clothes_2, weight_2 in lis_clothes_weight:
			if is_compatible_set_wash(set_clothes, map_clothes, clothes_2) and clothes_1 != clothes_2:
				set_clothes.add((clothes_2, weight_2))
				lis_clothes_weight.remove((clothes_2, weight_2))
		washeds.append(set_clothes)

	return washeds

def max_weight(washed):
	return max(washed, key=lambda item : item[1])

def total_weight(washeds):
	total_weight = 0
	for washed in washeds:
		total_weight += max_weight(washed)[1]
	return total_weight


def write_washed_file(name_in_file, name_out_file):
	washeds = build_lavados(name_in_file)
	count_lines = 0
	with open(name_out_file, 'w', encoding='utf-8') as out_file:
		for i, washed in enumerate(washeds):
			for clothes, weight in washed:
				if count_lines == 19:
					out_file.write("{} {}".format(clothes, str(i + 1)))
					break
				out_file.write("{} {}\n".format(clothes, str(i + 1)))
				count_lines += 1
	return

#washeds = build_lavados("primer_problema.txt")
#print(washeds)
#print("el peso del lavado total es: {}\n".format(total_weight(washeds)))

write_washed_file("primer_problema.txt", "97013.txt")