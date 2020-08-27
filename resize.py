import os
import numpy as np
import multiprocessing as mp
import tarfile, sys 
import cv2

src_dir='../dataset'
dst_dir='../dataset_rz'
rz_size = 244

def resize_func(src_path, dst_path):
    #print("untar {} => {}\n".format(src_path,dst_path))
    frame = cv2.imread(src_path,-1)
    rz_frame = cv2.resize(frame,(rz_size,rz_size),interpolation = cv2.INTER_CUBIC)
    rz_file_name=os.path.basename(src_path)
    rz_file_path=os.path.join(dst_path,rz_file_name)
    print("[{}=>{} ]rz_file_name = {}".format(src_path,dst_path,rz_file_name))

    cv2.imwrite(rz_file_path,rz_frame)

bookmark = 21415
dir_name_lists = np.sort(os.listdir(src_dir))
print("dir_name_lists = {}".format(dir_name_lists))
for dir_name in dir_name_lists:
    shot_num = int(dir_name)
    if shot_num > bookmark:
        dir_path = os.path.join(src_dir,dir_name)
        rz_dst_dir_path = os.path.join(dst_dir,dir_name)
        if not os.path.exists(rz_dst_dir_path):
            os.makedirs(rz_dst_dir_path)
            print("rz_dst_dir_path = {}".format(rz_dst_dir_path))

        if os.path.exists(dir_path):
            # print("dir_path = {} exiest".format(dir_path))
            pool = mp.Pool(mp.cpu_count())
            file_name_list = np.sort(os.listdir(dir_path))
            print(file_name_list)
            file_path_list = []
            for file_name in file_name_list:
                if file_name.lower().endswith("jpg"):
                    file_path= os.path.join(dir_path,file_name)
                    if os.path.exists(file_path):
                        file_path_list.append(file_path)
                        # print("append file name = {}".format(file_path))


            results = [pool.apply_async(resize_func, args=(file_path,rz_dst_dir_path))for file_path in file_path_list]
            pool.close()
            pool.join()



