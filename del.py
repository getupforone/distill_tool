import os
import numpy as np


rm_list_dir_path='../rmfilelist'
rm_img_dir_path='../rmimgs'


if os.path.isdir(rm_img_dir_path):
	print("rm_img_dir_path exists :{}".format(rm_img_dir_path)
else:
	os.mkdir(rm_img_dir_path)
	print("make rm_img_dir_path done :{}".format(rm_img_dir_path)


if os.path.exists(rm_img_dir_path)==False:
    os.mkdir(rm_img_dir_path)
    print("mkdir {}".format(rm_img_dir_path))
rm_lists = np.sort(os.listdir(rm_list_dir_path))

print(rm_lists)
for ind, rm_list in enumerate(rm_lists):
    shot_num = os.path.splitext(rm_list)[0]
    print(shot_num)
    rm_list_path = os.path.join(rm_list_dir_path, rm_list)

    if os.path.exists(rm_list_path):
        print("{} exist".format(rm_list_path))
        dst_path=os.path.join(rm_img_dir_path,shot_num)
        print("dst path={}".format(dst_path))
        if os.path.isdir(dst_path):
            print("dir {} exist".format(shot_num))
        else:
            print("dir {} does not exit".format(shot_num))
            os.mkdir(dst_path)
            
        with open(rm_list_path,'r') as file_read_obj:
            lines = file_read_obj.readlines()
            
            for idx, file_path in enumerate(lines):
                file_path = file_path.strip()  
                file_name=os.path.basename(file_path)
                
                #print("file_path :{}".format(file_path))
                src_path=file_path
                if os.path.exists(src_path):
                    print("filename={}".format(file_name))
                    print("dst path={}".format(dst_path))
                    dst_path2=os.path.join(dst_path,file_name)
                    print("dst path2={}".format(dst_path2))
                    print("mv {} => {}".format(src_path,dst_path2))
                    os.rename(src_path,dst_path2)
                else:
                    print("src_path {} does not exist".format(src_path))
                

                
            
                #assert os.path.exists(file_path), "{} dir not found".format(file_path)
                
    else:
        print("{} does not exist".format(rm_list_path))
    
