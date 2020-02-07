
import os
import numpy as np

dataset_paths = '../dataset'
dir_list_path='../dirlist'

train_ratio=80
test_ratio=15
val_ratio=5

if os.path.isdir(dir_list_path):
    print("dir_list_path exists :{}".format(dir_list_path))
else:
    os.mkdir(dir_list_path)
    print("make dir_list_path done :{}".format(dir_list_path))


dir_name_lists = np.sort(os.listdir(dataset_paths))
num_of_dir = len(dir_name_lists)
dir_path_lists = []
for idx, dir_name in enumerate(dir_name_lists):
	dir_path = os.path.join(dataset_paths,dir_name)
	dir_path = os.path.abspath(os.path.join(dataset_paths,dir_name))
	dir_path_lists.append(dir_path)
	print("dir_path_lists[{}]= {}".format(idx,dir_path))



print("num_of_dir = {}".format(num_of_dir))
num_of_train_dir = int(num_of_dir/100*train_ratio)
print("num_of_train_dir = {}".format(num_of_train_dir))
num_of_test_dir = int(num_of_dir/100*test_ratio)
print("num_of_test_dir = {}".format(num_of_test_dir))
num_of_val_dir = int(num_of_dir/100*val_ratio)
print("num_of_val_dir = {}".format(num_of_val_dir))

print("diff = {}".format(num_of_dir - num_of_train_dir -num_of_test_dir -num_of_val_dir))


train_path_lists = dir_path_lists[0:num_of_train_dir] # 0~ num_of_train_dir-1
print("num train_path_lists = {}".format(len(train_path_lists)))
print("train_path_lists = {}".format(train_path_lists))

test_path_lists = dir_path_lists[num_of_train_dir:num_of_train_dir + num_of_test_dir] #num_of_train_dir ~ num_of_train_dir + num_of_test_dir -1
print("num test_path_lists = {}".format(len(test_path_lists)))
print("train_path_lists = {}".format(test_path_lists))

val_path_lists = dir_path_lists[num_of_train_dir + num_of_test_dir:]
print("num test_path_lists = {}".format(len(val_path_lists)))
print("train_path_lists = {}".format(val_path_lists))

train_dir_list_name = "train.txt"
train_dir_list_path = os.path.join(dir_list_path,train_dir_list_name)

with open(train_dir_list_path, 'w') as file_write_obj:
	for train_path in train_path_lists:
		print("train_path is written to {} ={}".format(train_dir_list_path, train_path))
		lines = "{}\n".format(train_path)
		file_write_obj.writelines(lines)

test_dir_list_name = "test.txt"
test_dir_list_path = os.path.join(dir_list_path,test_dir_list_name)


with open(test_dir_list_path, 'w') as file_write_obj:
	for test_path in test_path_lists:
		print("test_path is written to {} ={}".format(test_dir_list_path, test_path))
		lines = "{}\n".format(test_path)
		file_write_obj.writelines(lines)

val_dir_list_name = "val.txt"
val_dir_list_path = os.path.join(dir_list_path,val_dir_list_name)


with open(val_dir_list_path, 'w') as file_write_obj:
	for val_path in val_path_lists:
		print("val_path is written to {} ={}".format(val_dir_list_path, val_path))
		lines = "{}\n".format(val_path)
		file_write_obj.writelines(lines)

