
import os
import numpy as np
print("thank you")

data_dir_paths = ['../dataset']
data_list_dir_path='../datalists'



if os.path.isdir(data_list_dir_path):
    print("data_list_dir_path exists :{}".format(data_list_dir_path))
else:
    os.mkdir(data_list_dir_path)
    print("make data_list_dir_path done :{}".format(data_list_dir_path))

for data_dir_path in data_dir_paths:
    dir_name_list = np.sort(os.listdir(data_dir_path))
    print("dir_name_list = P{}".format(dir_name_list))
    for ind, dir_name in enumerate(dir_name_list):
        
        dir_path = os.path.abspath(os.path.join(data_dir_path,dir_name))
        if os.path.isdir(dir_path):
            #line = "{}".format(dir_path)
           
            file_name_list = np.sort(os.listdir(dir_path))
            seq_list_file_name = "{}.txt".format(dir_name)
            seq_list_file_path = os.path.join(data_list_dir_path, seq_list_file_name)
            
            file_write_obj = open(seq_list_file_path,'w')
            for ind, file_name in enumerate(file_name_list):
                file_path = os.path.join(dir_path,file_name)
                line = "{}".format(file_path)
                if line.lower().endswith(('.bmp','.png', '.jpg', '.jpeg')):
                    print(line)
                    file_write_obj.writelines(line)
                    #file_write_obj.writelines(seq)
                    file_write_obj.write('\n')


            file_write_obj.close()
        
