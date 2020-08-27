
import os
import numpy as np
import random


data_dir_paths = ['../dataset']
data_list_dir_path='../datalists'
data_img_list_dir_path='/data/KSTAR_TV_DATASET/imglist_3label'
cnt_label_path='../cntlabel/threelabel.txt'

disrupt_th = 21
train_ratio=80
test_ratio=15
val_ratio=5

if os.path.isdir(data_list_dir_path):
    print("data_list_dir_path exists :{}".format(data_list_dir_path))
else:
    os.mkdir(data_list_dir_path)
    print("make data_list_dir_path done :{}".format(data_list_dir_path))


dir_path_lists = []
dir_label_lists = []
shotnum_list = []
index_shotnum_dic = {}
if os.path.exists(cnt_label_path):
    with open(cnt_label_path, 'r') as file_read_obj:
        #lines = file_read_obj.read().splitlines())
        for idx, path_label in enumerate(file_read_obj.read().splitlines()):
            assert len(path_label.split()) == 2
            path, label = path_label.split()
            dir_path_lists.append(path)
            num_of_dir = len(dir_path_lists)
            #print(label)
            # if label== "True":
            #     true_cnt = true_cnt +1;
            # elif label=="False":
            #     false_cnt = false_cnt +1;
            # elif label=="Disrupt":
            #     disrupt_cnt = disrupt_cnt +1;
            dir_label_lists.append(label)
            shot_num= os.path.splitext(os.path.splitext(os.path.basename(path))[0])[0]
            # print(shot_num)
            index_shotnum_dic[shot_num]=idx
            shotnum_list.append(shot_num)

            # print(index_shotnum_dic)
            #print("path = {}/ label = {}\n".format(path,label))
else:
    print("cnt_label_path {} does not exist".format(cnt_label_path))

print("num_of_dir = {}".format(num_of_dir))
num_of_train_dir = int(num_of_dir/100*train_ratio)
print("num_of_train_dir = {}".format(num_of_train_dir))
num_of_test_dir = int(num_of_dir/100*test_ratio)
print("num_of_test_dir = {}".format(num_of_test_dir))
num_of_val_dir = int(num_of_dir/100*val_ratio)
print("num_of_val_dir = {}".format(num_of_val_dir))

print("diff = {}".format(num_of_dir - num_of_train_dir -num_of_test_dir -num_of_val_dir))

random_index = random.sample(range(0,num_of_dir),num_of_dir)
shotnum_list_np = np.array(shotnum_list)
shotnum_list_rand = shotnum_list_np[random_index]


train_shotnum_lists = shotnum_list_rand[0:num_of_train_dir] # 0~ num_of_train_dir-1

print("num train_shotnum_lists = {}".format(len(train_shotnum_lists)))
# print("train_shotnum_lists = {}".format(train_shotnum_lists))

test_shotnum_lists = shotnum_list_rand[num_of_train_dir:num_of_train_dir + num_of_test_dir] #num_of_train_dir ~ num_of_train_dir + num_of_test_dir -1
print("num test_shotnum_lists = {}".format(len(test_shotnum_lists)))
# print("train_shotnum_lists = {}".format(test_shotnum_lists))

val_shotnum_lists = shotnum_list_rand[num_of_train_dir + num_of_test_dir:]

print("num test_shotnum_lists = {}".format(len(val_shotnum_lists)))
# print("train_shotnum_lists = {}".format(val_shotnum_lists))

train_dir_name = 'train'
train_dir_path = os.path.abspath(os.path.join(data_img_list_dir_path,train_dir_name))

test_dir_name = 'test'
test_dir_path = os.path.abspath(os.path.join(data_img_list_dir_path,test_dir_name))

val_dir_name = 'val'
val_dir_path = os.path.abspath(os.path.join(data_img_list_dir_path,val_dir_name))
dir_path_list = [train_dir_path,test_dir_path,val_dir_path]

for dir_path in dir_path_list:
    print(dir_path)
    if os.path.isdir(dir_path):
        print("data_list_dir_path exists :{}".format(dir_path))
    else:
        os.mkdir(dir_path)
        print("make data_list_dir_path done :{}".format(dir_path))

for data_dir_path in data_dir_paths:
    dir_name_list = np.sort(os.listdir(data_dir_path))
    # print("dir_name_list = P{}".format(dir_name_list))
    for ind, dir_name in enumerate(dir_name_list):
        if dir_name in index_shotnum_dic:         
            src_dir_path = os.path.abspath(os.path.join(data_dir_path,dir_name))
            curr_shotnum = dir_name
            curr_idx = index_shotnum_dic[curr_shotnum]
       
            if os.path.isdir(src_dir_path):
               file_name_list = np.sort(os.listdir(src_dir_path))
              
               curr_label = dir_label_lists[curr_idx]
            #    print(curr_label)
               seq_list_file_name = "{}.txt".format(dir_name)
               seq_list_file_name_D = "{}_D.txt".format(dir_name)
               cat_name = 'train'
               if curr_shotnum in train_shotnum_lists :
                   cat_name = 'train'
               elif curr_shotnum in test_shotnum_lists :
                   cat_name = 'test'
               elif curr_shotnum in val_shotnum_lists :
                   cat_name = 'val'
               seq_list_file_path = os.path.join(os.path.join(data_img_list_dir_path,cat_name), seq_list_file_name)
               seq_list_file_path_D = os.path.join(os.path.join(data_img_list_dir_path,cat_name), seq_list_file_name_D)
               num_of_file = len(file_name_list)
               
               true_label_num = num_of_file - disrupt_th
               if true_label_num  > 0:
                file_write_obj = open(seq_list_file_path,'w')
                if curr_label == 'Disrupt':
                    file_write_obj_D = open(seq_list_file_path_D,'w')
                for f_ind, file_name in enumerate(file_name_list):
                    f_label = curr_label
                    file_path = os.path.join(src_dir_path,file_name)
                    if curr_label == 'Disrupt':
                        if f_ind > true_label_num :
                            f_label = 'Disrupt'     
                            line = "{}   {}".format(file_path,f_label)    
                            file_write_obj_D.write('\n')
                            file_write_obj_D.writelines(line)               
                        else :
                            f_label = 'True'
                            line = "{}   {}".format(file_path,f_label)
                            file_write_obj.write('\n')
                            file_write_obj.writelines(line)
                    elif curr_label != 'Disrupt':
                        line = "{}   {}".format(file_path,f_label)
                        file_write_obj.write('\n')
                        file_write_obj.writelines(line)



        
