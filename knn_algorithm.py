from random import randint
from math import floor

def load_instances(file_path, percentage):
	file = open(file_path, "r")
	training_file = open("instances/training_file.txt", "w")
	testing_file = open("instances/testing_file.txt", "w")

	random_index_vet = []
	training_vet = []

	count_lines = 0
	for line in file:
		line = line.strip()
		list_aux = line.split(",")
		training_vet.append(list_aux)
		count_lines += 1
	for i in range(len(training_vet)):
		print(i, " - ", training_vet[i])

	for _ in range(floor(percentage*count_lines)):
		random_num = randint(0,count_lines-1)
		while(random_num in random_index_vet):
			random_num = randint(0,count_lines-1)
		random_index_vet.append(random_num)
	random_index_vet.sort()

	for index in random_index_vet:
		agg_list = ",".join(training_vet[index]) + "\n"
		testing_file.write(agg_list)
		training_vet[index] = None
	
	training_vet = list(filter((None).__ne__, training_vet))

	for train in training_vet:
		train = ",".join(train) + "\n"
		training_file.write(train)

	file.close()
	training_vet.close()
	training_file.close()

	return training_vet

# Function to calculate euclidian distance
def euc_distance(x1, x2):
	return (x1 - x2)**2

def knn_algorithm(k_param, training_vet):
	pass

load_instances("instances/car_instances.txt", 0.4)