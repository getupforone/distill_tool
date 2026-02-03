import cv2

import os
import numpy as np
from matplotlib import pyplot as plt
import multiprocessing as mp

from cntlable import cnt_label
from list_path_div import gen_path_list
from del_rmfile import del_rmfile

def calc_brightness():
    brightness 
    return brightness

def write_text(img,str):
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,500)
    fontScale              = 1
    fontColor              = (255,255,255)
    lineType               = 2

    cv2.putText(img,str, 
    bottomLeftCornerOfText, 
    font, 
    fontScale,
    fontColor,
    lineType)


fig_paths = './figs'




def init():
	if os.path.isdir(data_list_dir_path):
		print("data_list_dir_path exists :{}".format(data_list_dir_path))
	else:
		os.mkdir(data_list_dir_path)
		print("make data_list_dir_path done :{}".format(data_list_dir_path))

	if os.path.isdir(fig_paths):
		print("fig_paths exists :{}".format(fig_paths))
	else:
		os.mkdir(fig_paths)
		print("make fig_paths done :{}".format(fig_paths))

	if os.path.isdir(rm_list_dir_path):
		print("rm_list_dir_path exists :{}".format(rm_list_dir_path))
	else:
		os.mkdir(rm_list_dir_path)
		print("make rm_list_dir_path done :{}".format(rm_list_dir_path))

def bright_filter(dataset_dir_paths= ['./dataset'], data_list_dir_path='./imgpathlist', rm_list_dir_path='./rmfilelist'):
    # dataset_dir_paths = ['./dataset']
    # data_list_dir_path='./imgpathlist'
    # rm_list_dir_path='./rmfilelist'
    img_margin = 50
    bri_th = 10
    img_cut_th = 1

    mode_dir_path = np.sort(os.listdir(data_list_dir_path)) 
    # mode_dir_path = [./imgpathlist/train,./imgpathlist/test,./imgpathlist/val]

    all_file_name_list = []
    for mode_dir_path in mode_dir_path:
        if os.path.isdir(mode_dir_path):
            file_name_list = np.sort(os.listdir(mode_dir_path))
            all_file_name_list.extend(file_name_list)


    for file_list_path in all_file_name_list:
        # file_list_path = 019819.txt ...
        rm_list_path = os.path.abspath(os.path.join(rm_list_dir_path,os.path.splitext(file_list_path)[0]+".txt"))
        print(rm_list_path)

        
        with open(file_list_path,'r') as file_read_obj:
            
            lines = file_read_obj.readlines()
            # file_path = /Users/giilkwon/WorkSpace/KSTAR_TV_DATASET/dataset_rz/019835/019835-00028.jpg   True
            #brightness_arr = np.zeros(len(lines))
            brightness_arr=[]
            brigharea_cnt_arr=[]
            rm_file_path_list = []
            for idx, file_path_label in enumerate(lines):
                print("file_path_label :{}".format(file_path_label))
                file_path = file_path_label.strip().split()[0]
                print("file_path :{}".format(file_path))
                assert os.path.exists(file_path), "{} dir not found".format(file_path)

                src = cv2.imread(file_path)
                img = src[img_margin:-img_margin,img_margin:-img_margin]
                if img is None:
                    print("image is none")
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                mask = np.zeros(gray.shape,dtype=np.uint8)
                mask[gray > bri_th ] = 255
                mask[gray <= bri_th ] = 0
                # cnt_black = gray < bri_th
                # gray_black = gray[gray < bri_th ] 
                # avg_gray = np.average(gray_black)
                # print("avg_gray = {}".format(avg_gray))
                avg = np.average(gray)
                brightness_arr.append(avg)
                cnt = cv2.countNonZero(mask)
                brigharea_cnt_arr.append(cnt)

                if avg < img_cut_th:
                    # write_text(gray,'CUT')
                    rm_file_path_list.append(file_path)
                # else:
                #     write_text(gray,'reserve')
                            
            # plt.subplot(211)

            # plt.plot(brightness_arr)
            # plt.grid()
            # plt.subplot(212)

            # plt.plot(brigharea_cnt_arr)
            # plt.grid()
            # with open(rm_list_path,'w') as file_write_obj:
            #     for rm_file_path in rm_file_path_list:
            #         line="{}\n".format(rm_file_path)
            #         file_write_obj.writelines(line)
            # fig_path = os.path.splitext(data_list)
            # fig_path = os.path.join(fig_paths,fig_path[0])
            # print("fig_path : {}".format(fig_path))
            # plt.savefig(fig_path, dpi=500)
            # plt.clf()

if __name__ == "__main__":
    dataset_dir_paths = ['../dataset_rz']
    result_dir_path = '../results'
    if not os.path.exists(result_dir_path):
        os.makedirs(result_dir_path)
    data_list_dir_path=f'{result_dir_path}/imgpathlist'
    if not os.path.exists(data_list_dir_path):
        os.makedirs(data_list_dir_path)
    cnt_label_dir_path=f'{result_dir_path}/cntlabel'
    if not os.path.exists(cnt_label_dir_path):
        os.makedirs(cnt_label_dir_path)

    cnt_label_path=os.path.join(cnt_label_dir_path,"cntlabel.txt")
    rm_list_dir_path=f'{result_dir_path}/rmfilelist'
    if not os.path.exists(rm_list_dir_path):
        os.makedirs(rm_list_dir_path)
    rm_img_dir_path=f'{result_dir_path}/rmimgs'
    if not os.path.exists(rm_img_dir_path):
        os.makedirs(rm_img_dir_path)

    cnt_label(dataset_dir_paths, result_dir_path)
    print("cnt_label done")
    gen_path_list(dataset_dir_paths, data_list_dir_path, cnt_label_path)  
    print("gen_path_list done")
    bright_filter(dataset_dir_paths, data_list_dir_path, rm_list_dir_path)
    print("bright_filter done")
    del_rmfile(rm_list_dir_path, rm_img_dir_path)
    print("del_rmfile done")

# break_key = False
# init()
# num_cpu_cores = mp.cpu_count()
# print("num of cpu is {}: ".format(num_cpu_cores))

# pool = mp.Pool(mp.cpu_count())
# data_lists = np.sort(os.listdir(data_list_dir_path))

# results = [pool.apply_async(bright_filter, args=(data_list,))for data_list in data_lists]
        
# pool.close()   
# pool.join()


