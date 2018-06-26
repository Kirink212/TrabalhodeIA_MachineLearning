from random import randint
from math import floor, sqrt
from random import shuffle
from collections import defaultdict
from time import time

# Defines file's directory path
file_directory = "instances/"

# Writes an array content in a file
# In this case, each array element is of type "list"
def write_array_in_file(array, file_path):
	file = open(file_directory + file_path, "w")

	for el in array:
		el = ",".join(el) + "\n"
		file.write(el)

	file.close()

# Load instances, splitting, depending on percentage,
# how many will be registered as train or test instances
def load_instances(file_path, percentage):
	# Open instances file
	file = open(file_path, "r")

	# Initializes training array
	training_vet = []

	# For each line in file, split's its elements
	# and insert them, as a list, on training_vet
	# The total number of lines are also counted
	count_lines = 0
	for line in file:
		line = line.strip()
		list_aux = line.split(",")
		training_vet.append(list_aux)
		count_lines += 1

	# Randomize training_vet elements,
	# not letting them to be sorted by 
	# classification or attribute
	shuffle(training_vet)

	# Defines the limit index, splitting
	# training_vet in a training array and
	# a testing array
	limit = floor(percentage*count_lines)
	training_array = training_vet[limit:]
	testing_array = training_vet[:limit]

	# For each element in training array write it in a file
	write_array_in_file(training_array, "training_file.txt")

	# For each element in testing array write it in a file
	write_array_in_file(testing_array, "testing_file.txt")

	# Close file
	file.close()

	return training_array, testing_array

# Function to calculate distance between categoric attributes
def attribute_distance(test, train, total_attr):
	# Distance sum is initialized with 0
	distance_sum = 0

	# For each attribute, verify if they're different;
	# If TRUE, the distance between them is 1 (100%);
	# If FALSE, the distance between them is 0 (0%);
	# The total "distance" is inserted to distance_sum.
	for index in range(total_attr):
		if test[index] != train[index]:
			distance_sum += 1
		else:
			distance_sum += 0

	return distance_sum

def knn_algorithm(k_param, testing_vet, training_vet):
	t0 = time()
	# For each testing instance
	for (index1, test) in enumerate(testing_vet):
		# Initializes a distance vet for each testing
		# instance
		distance_vet = []

		# For each training instance
		for (index2, train) in enumerate(training_vet):

			# Verify total distance between attributes
			distance = attribute_distance(test, train, len(test)-1)
			# Measuring EUCLIDEAN's distance, calculating the square
			# root of the total distance
			distance = sqrt(distance)
			# Insert 
			distance_vet.append([distance, index2])

		# Sorting distance_vet in ascending order
		distance_vet.sort()

		# Verifies if k_param surpasses distance_vet's length;
		# If TRUE, copies all distance_vet to k_distances;
		# If FALSE, copies from the first to the kth distance
		# insisde distance_vet.
		if k_param > len(distance_vet):
			k_distances = distance_vet[:]
		else:
			k_distances = distance_vet[:k_param]
		
		# Defines class_vet as a int dictionary
		class_vet = defaultdict(int)

		# For each distance, count the total of
		# instances that are classified by each
		# class name
		for k_dist in k_distances:
			curr_index = k_dist[1]
			curr_train = training_vet[curr_index]
			class_pos = len(curr_train)-1
			class_name = curr_train[class_pos]

			if class_name not in class_vet:
				class_vet[class_name] = 1
			else:
				class_vet[class_name] += 1

		# Initialize the class name with most training 
		# instances near current test instance, and register
		# the total number of instances that are classified
		# with predicted_class_name
		predicted_class_total = None
		predicted_class_name = None
		
		for (class_name, n_neighbors) in class_vet.items():
			if not predicted_class_total:
				predicted_class_total = n_neighbors
				predicted_class_name = class_name
			else:
				if n_neighbors > predicted_class_total:
					predicted_class_total = n_neighbors
					predicted_class_name = class_name
		test.append(predicted_class_name)
	t1 = time()

	print("Tempo de execução: %fs"%(t1-t0))
	return testing_vet

def test_knn(test_file_path, k_param, v_test, v_train):
	test_file = open(file_directory + test_file_path, "r")
	testing_vet = knn_algorithm(k_param, v_test, v_train)

	incorrect = 0
	correct = 0
	total = len(testing_vet)
	for el in testing_vet:
		curr_line = test_file.readline()
		list_aux = curr_line.split(",")
		class_pos_real = len(list_aux)-1
		class_pos_pred = len(el)-1
		class_name_pred = el[class_pos_pred].strip()
		class_name_real = list_aux[class_pos_real].strip()
		# print("Previsto: ", class_name_pred)
		# print("Real: ", class_name_real)
		# print("Igual? ", (class_name_pred == class_name_real))
		if class_name_pred == class_name_real:
			correct += 1
		else:
			incorrect += 1

	print("Correct: %.2f%%"%((correct*100.0)/total))
	print("Incorrect: %.2f%%"%((incorrect*100.0)/total))

def k_means_algorithm(k_param, testing_vet, training_vet):
	k_instances = []

	pass

v_train, v_test = load_instances(file_directory + "car_instances.txt", 0.40)
test_knn("testing_file.txt", 1200, v_test, v_train)