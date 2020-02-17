import os
import numpy as np
from matplotlib import pyplot as plt

label_dir_path="../cntlabel"
label_file_name = "cntlabel.txt"
data_dir_paths = ['../dataset']
file_num_dict = {}
cnt_label_dict = {}
cnt_threshold = 500
true_label_cnt = 0
false_label_cnt = 0
for data_dir_path in data_dir_paths:
    if os.path.isdir(data_dir_path):
        dir_name_list = np.sort(os.listdir(data_dir_path))
        #print("dir_name_list = {}".format(dir_name_list))
        for ind, dir_name in enumerate(dir_name_list):
            dir_path = os.path.abspath(os.path.join(data_dir_path, dir_name))
            print("dir_path[{}] = {}".format(ind,dir_path))
            if os.path.isdir(dir_path):
                file_name_list = np.sort(os.listdir(dir_path))
                num_of_files = len(file_name_list)
                file_num_dict[dir_name] = num_of_files
                if num_of_files > cnt_threshold :
                    cnt_label_dict[dir_name] = (dir_path,True)
                    true_label_cnt = true_label_cnt + 1
                else:
                    cnt_label_dict[dir_name] = (dir_path,False)
                    false_label_cnt = false_label_cnt + 1
    
    label_file_path = os.path.join(label_dir_path, label_file_name)
    with open(label_file_path, 'w') as file_write_obj:
        for k,v in cnt_label_dict.items():
            (dir_path, label) = v
            lines="{}   {}\n".format(v[0], v[1])
            print(lines)
            file_write_obj.writelines(lines)
print("true label = {} / false label = {}".format(true_label_cnt, false_label_cnt))

isPlot = False

if isPlot == True:
    dir_name_list = []
    file_num_list = []
    for dir_name, file_num in file_num_dict.items():
        print("file_ num[{}] = {}".format(dir_name, file_num))
        dir_name_list.append(dir_name)
        file_num_list.append(file_num)
    
    plt.plot(file_num_list)
    plt.grid()
    plt.show()
