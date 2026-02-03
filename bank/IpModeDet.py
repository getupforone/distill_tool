#from MDSplus import *
#from MDSplus import Connection
import matplotlib
from matplotlib.pyplot import plot, xlim, show
from matplotlib import pyplot as plt
import argparse
import pickle
import os
import numpy as np
import multiprocessing as mp

pickle_dir_path = '../rc03_data'
fig_paths = '../figs/ip'

def avg(lst):
	return sum(lst) / len(lst)
def main(use_argparse=False,show_plot=False,save_plot=False):
	shot = 19931 
	tree = 'kstar'
	tag='\\RC03'
	
	if use_argparse == True:
		parser = argparse.ArgumentParser(description='shot tree')
		parser.add_argument("shot", help="shot number", type=int, default=0)		
		parser.add_argument("window", help="size of window",type=int, default='5')

		args =  parser.parse_args()
		shot = args.shot
		window = args.window
		print("{}/{}".format(shot,window))


	if os.path.isdir(pickle_dir_path):
		print("pickle_dir_path :{}".format(pickle_dir_path))
	else:
		print("pickle_dir_path does not exit")
		return false
	if os.path.isdir(fig_paths):
		print("fig_paths exists :{}".format(fig_paths))
	else:
		os.mkdir(fig_paths)
		print("make fig_paths done :{}".format(fig_paths))
	pickle_name_lists = np.sort(os.listdir(pickle_dir_path))
	num_of_dir = len(pickle_name_lists)
	pickle_path_lists = []
	for idx, pickle_name in enumerate(pickle_name_lists):
		pickle_path = os.path.abspath(os.path.join(pickle_dir_path, pickle_name))
		pickle_path_lists.append(pickle_path)
		#print("pickle_path_lists[{}] = {}".format(idx, pickle_path))

	#pickle_name="rc03_{}.pickle".format(shot)	
	#pickle_path = os.path.join(pickle_dir_path,pickle_name)
	#print(pickle_path)

	num_cpu_cores = mp.cpu_count()
	print("num of cpu is {}: ".format(num_cpu_cores))
        
	for pickle_path in pickle_path_lists:
			draw(pickle_path)
	#pool = mp.Pool(mp.cpu_count())
	#
        #
	#results = [pool.apply_async(det, args=(pickle_path,))for pickle_path in pickle_path_lists]
	#	
	#pool.close()   
	#pool.join()

def det(pickle_path,show_plot=False,save_plot=True):
	dwsp_window = int(500/2)
	window = 10
	window2 = 20
	
	print(pickle_path)
	if os.path.exists(pickle_path):
		print("pickle_path exists :{}".format(pickle_path))

	with open(pickle_path, 'rb') as f:
		data = pickle.load(f,encoding='latin1')
		
		v = data['value'] 
		t = data['time']
		v_len = len(v)
		dwsp_ind = range(v_len)
		v2 = []
		t2 = []

		for ii in dwsp_ind[dwsp_window: -dwsp_window:dwsp_window]:
			dwsp_v = (avg(v[ii-dwsp_window:ii+dwsp_window]))
			v2.append(dwsp_v)
			t2.append(t[ii])

		v_len2 = len(v2)
		ind = range(v_len2)
		grads = [0]*v_len2
		grads2=[None]*v_len2

		cls_1 = []
		cls_2 = []
		cls_3 = []
		cls_4 = []
		cls_pts=[None]*v_len2

		for i in ind[window: -window]:
			#print(v[i-window:i+window])
			lv = v2[i-window:i]
			rv = v2[i:i+window]

			ld = []
			rd = []
			for ii in range(window):
				ld.append(lv[-1] - lv[ii])
				rd.append(rv[0] - rv[ii])
			lgrad = det_grad(ld,window)
			rgrad = det_grad(rd,window)

			if (lgrad>0) and (rgrad<0):
				grads[i] = 2
			elif (lgrad<0) and(rgrad>0):
				grads[i] = 1
			elif (lgrad==0) or (rgrad==0):
				grads[i] = 0
			else:
				grads[i] = 0
		t_lim = [-1.0,9.0]
		for i in ind[window2: -window2]:
			lg = grads[i-window2:i]
			rg = grads[i:i+window2]

			lgrad2 = det_grad2(lg,window2)
			rgrad2 = det_grad2(rg,window2)
			if (lgrad2 == 0)  and (rgrad2 == 2) :
				grads2[i] = 4
				if t2[i] >= t_lim[0] and t2[i] <= t_lim[1]:
					cls_4.append(i)
			elif (lgrad2 == 2) and (rgrad2 == 0) :
				grads2[i] = 3
				if t2[i] >= t_lim[0] and t2[i] <= t_lim[1] :
					cls_3.append(i)
			elif (lgrad2 == 0) and (rgrad2 == 1) :
				grads2[i] = 2
				if t2[i] >= t_lim[0] and t2[i] <= t_lim[1]:
					cls_2.append(i)
			elif (lgrad2 == 1) and (rgrad2 == 0):
				grads2[i] = 1
				if t2[i] >= t_lim[0] and t2[i] <= t_lim[1]:
					cls_1.append(i)
			else:
				grads2[i] = None
		
		cls_4_lm = cls_4[0]
		#print("cls_4 :",cls_4)
		#print(cls_4_lm)
		
		#print("cls_3 :",cls_3)
		#print(cls_3_rm)
		
		#print("cls_2 :",cls_2)
		#print(cls_2_lm)

		cls_1_lm = cls_1[0]
		#print("cls_1 :",cls_1)
		#print(cls_1_lm)
		cls_3_2 = []
		cls_2_2 = []
		for c3 in cls_3:
			if (c3 >= cls_4_lm) and (c3 <= cls_1_lm):
				cls_3_2.append(c3)
		for c2 in cls_2:
			if (c2 >= cls_4_lm) and (c2 <= cls_1_lm):
				cls_2_2.append(c2)
		


		cls_3_rm = cls_3_2[-1]
		cls_2_lm = cls_2_2[0]
		print("cls_3 :",cls_3)
		print(cls_3_rm)
		
		print("cls_2 :",cls_2)
		print(cls_2_lm)


		cls_4_tup = (cls_4_lm,4)
		cls_3_tup = (cls_3_rm,3)
		cls_2_tup = (cls_2_lm,2)
		cls_1_tup = (cls_1_lm,1)
		cls_tup = [cls_4_tup, cls_3_tup, cls_2_tup, cls_1_tup]
		t3 = [t2[cls_tup[0][0]],t2[cls_tup[1][0]],t2[cls_tup[2][0]],t2[cls_tup[3][0]]]
		v3 = [v2[cls_tup[0][0]],v2[cls_tup[1][0]],v2[cls_tup[2][0]],v2[cls_tup[3][0]]]
		c3 = [cls_tup[0][1],cls_tup[1][1],cls_tup[2][1],cls_tup[3][1]]
		print(t3)
		print(v3)
		print(c3)
		

		for ct in cls_tup:
			cls_pts[ct[0]] = ct[1]
			print("{}/{}".format(ct[0], ct[1]))
			print("cls_pts[{}]= {}".format(ct[0], ct[1]))
		print(len(cls_pts))
		print("cls_pts[{}] ={}".format(cls_tup[0],cls_pts[cls_tup[0][0]]))
		print("cls_pts[{}] ={}".format(cls_tup[1],cls_pts[cls_tup[1][0]]))
		print("cls_pts[{}] ={}".format(cls_tup[2],cls_pts[cls_tup[2][0]]))
		print("cls_pts[{}] ={}".format(cls_tup[3],cls_pts[cls_tup[3][0]]))
		#print("{} || {}".format(lv,rv))
		#print(v)
		#plt.figure(figsize=(12,4))
		#plt.plot(t,v)
		plt.plot(t2,v2,lw=1)
		#plt.plot(t,v);
		#plt.scatter(t,v)
		plt.scatter(t2,v2,c=grads, s=10, cmap=plt.cm.get_cmap('rainbow',3), alpha=0.8)
		#plt.colorbar(ticks=range(3),format='color: %d', label='color')
		colors = ['green','blue','purple','red']
		plt.scatter(t2,v2,c=grads2, s=100, cmap=matplotlib.colors.ListedColormap(colors), alpha=0.5)
		#plt.scatter(t2,v2,c=cls_pts, s=500, cmap=matplotlib.colors.ListedColormap(colors), alpha=0.5)
		plt.plot(t3,v3)
		plt.scatter(t3,v3,c=c3, s=500, cmap=matplotlib.colors.ListedColormap(colors), alpha=0.5)
		fig_path = os.path.splitext(pickle_path)
		fig_name = os.path.basename(fig_path[0])
		print("fig_path :{}".format(fig_path))
		print("fig_paths :{}".format(fig_paths))
		print("fig_name :{}".format(fig_name))
		fig_name2="{}.png".format(fig_name)
		fig_path = os.path.join(fig_paths,fig_name2)
		print("fig_path :{}".format(fig_path))
		#print("fig_paths :{}".format(fig_paths))

		#plt.colorbar(ticks=range(4),format='color: %d', label='color')
		if save_plot== True:
			print("save_plot to {}".format(fig_path))
			plt.savefig(fig_path, dpi=500)
			#xlim(-1.0,9.0);
		if show_plot == True:
			plt.show();
			# plot(t,v)
			# show()
def draw(pickle_path,show_plot=True,save_plot=False):
	dwsp_window = int(500/2)
	window = 10
	window2 = 20
	
	print(pickle_path)
	if os.path.exists(pickle_path):
		print("pickle_path exists :{}".format(pickle_path))

	with open(pickle_path, 'rb') as f:
		data = pickle.load(f,encoding='latin1')
		
		v = data['value'] 
		t = data['time']
		v_len = len(v)
		dwsp_ind = range(v_len)
		v2 = []
		t2 = []

		for ii in dwsp_ind[dwsp_window: -dwsp_window:dwsp_window]:
			dwsp_v = (avg(v[ii-dwsp_window:ii+dwsp_window]))
			v2.append(dwsp_v)
			t2.append(t[ii])

		v_len2 = len(v2)
		ind = range(v_len2)
		#plt.figure(figsize=(12,4))
		#plt.plot(t,v)
		plt.plot(t2,v2,lw=1)
		
		#plt.plot(t,v);
		#plt.scatter(t,v)
		fig_path = os.path.splitext(pickle_path)
		fig_name = os.path.basename(fig_path[0])
		print("fig_path :{}".format(fig_path))
		print("fig_paths :{}".format(fig_paths))
		print("fig_name :{}".format(fig_name))
		fig_name2="{}.png".format(fig_name)
		fig_path = os.path.join(fig_paths,fig_name2)
		print("fig_path :{}".format(fig_path))
		plt.title(fig_name)
		#print("fig_paths :{}".format(fig_paths))
		xlim(-1.0,10.0);
		#plt.colorbar(ticks=range(4),format='color: %d', label='color')
		if save_plot== True:
			print("save_plot to {}".format(fig_path))
			plt.savefig(fig_path, dpi=500)
			
		if show_plot == True:
			plt.show();
			# plot(t,v)
			# show()

def det_grad2(grads,window):
	cnt_cls_0 = 0
	cnt_cls_1 = 0
	cnt_cls_2 = 0
	for grd in grads:
		cnt_cls_0 = (cnt_cls_0 + 1) if grd == 0 else cnt_cls_0
		cnt_cls_1 = (cnt_cls_1 + 1) if grd == 1 else cnt_cls_1
		cnt_cls_2 = (cnt_cls_2 + 1) if grd == 2 else cnt_cls_2

	
	cnt_clss = [cnt_cls_0, cnt_cls_1, cnt_cls_2]
	min_cls_idx = cnt_clss.index(min(cnt_clss))
	max_cls_idx = cnt_clss.index(max(cnt_clss))
	max_cnt = cnt_clss[max_cls_idx]
	del cnt_clss[min_cls_idx]
	max_cls_idx2 = cnt_clss.index(max(cnt_clss))
	del cnt_clss[max_cls_idx2]
	grad2 = 0
	diff = max_cnt - cnt_clss[0]
	if diff >= window - 1:
		grad2 = max_cls_idx
	else:
		grad2= 0
	return grad2


def det_grad(diff,window):
	cnt_m = 0
	cnt_p = 0
	grad = 0
	for df in diff:
		cnt_m = (cnt_m + 1) if df < 0 else cnt_m
		cnt_p = (cnt_p + 1) if df > 0 else cnt_p
	if cnt_m - cnt_p  >=  window-1:
		grad = -1
	elif cnt_m - cnt_p <=  window -1:
		grad = 1
	return grad



if __name__ == "__main__":
	main(False,False,True)
