import cv2

import os
import numpy as np
from matplotlib import pyplot as plt

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


fig_paths = '../figs'
data_dir_paths = ['../dataset']
data_list_dir_path='../datalists'
rm_list_dir_path='../rmfilelist'

if os.path.isdir(data_list_dir_path):
	print("data_list_dir_path exists :{}".format(data_list_dir_path)
else:
	os.mkdir(data_list_dir_path)
	print("make data_list_dir_path done :{}".format(data_list_dir_path)

if os.path.isdir(fig_paths):
	print("fig_paths exists :{}".format(fig_paths)
else:
	os.mkdir(fig_paths)
	print("make fig_paths done :{}".format(fig_paths)

if os.path.isdir(rm_list_dir_path):
	print("rm_list_dir_path exists :{}".format(rm_list_dir_path)
else:
	os.mkdir(rm_list_dir_path)
	print("make rm_list_dir_path done :{}".format(rm_list_dir_path)


img_margin = 50
bri_th = 10
img_cut_th = 1
data_lists = np.sort(os.listdir(data_list_dir_path))
break_key = False

for ind, data_list in enumerate(data_lists):
    rm_list_path = os.path.abspath(os.path.join(rm_list_dir_path,os.path.splitext(data_list)[0]+".txt"))
    print(rm_list_path)
    data_list_path = os.path.abspath(os.path.join(data_list_dir_path,data_list))
    print("data_list = {}".format(data_list_path))
    
    with open(data_list_path,'r') as file_read_obj:
        
        lines = file_read_obj.readlines()

        #brightness_arr = np.zeros(len(lines))
        brightness_arr=[]
        brigharea_cnt_arr=[]
        rm_file_path_list = []
        for idx, file_path in enumerate(lines):
            print("file_path :{}".format(file_path))
            file_path = file_path.strip()
            #print(os.path.exists(file_path))
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
            # plt.show(False)
            # plt.draw()
            # print("avg = {}".format(avg))
            # height, width, channels = img.shape
            # print("img size = {}/{}/{}".format(height, width, channels ))
            # cv2.imshow('image',img)
            # cv2.imshow('gray',gray)
            # cv2.imshow('mask', mask)
            
            # k = cv2.waitKey(0) 
            # if (k  & 0xFF )== ord('q'):
            #     break_key = True
            #     break
            # elif (k & 0xFF) == ord('n'):
            #     break_key = False
            #     break
            #cv2.destroyAllWindows()
        plt.subplot(211)

        plt.plot(brightness_arr)
        plt.grid()
        plt.subplot(212)

        plt.plot(brigharea_cnt_arr)
        plt.grid()
        with open(rm_list_path,'w') as file_write_obj:
            for rm_file_path in rm_file_path_list:
                line="{}\n".format(rm_file_path)
                file_write_obj.writelines(line)
        fig_path = os.path.splitext(data_list)
        fig_path = os.path.join(fig_paths,fig_path[0])
        print("fig_path : {}".format(fig_path))
        plt.savefig(fig_path, dpi=300)
        plt.clf()
    if break_key == True:
        break        
    




