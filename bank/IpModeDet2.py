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
def main(use_argparse=True,show_plot=False,save_plot=False):
	shot = 19931 
	tree = 'kstar'
	tag='\\RC03'
	
	if use_argparse == True:
		parser = argparse.ArgumentParser(description='shot tree')
		parser.add_argument("shot", help="shot number", type=int, default=0)		
		#parser.add_argument("window", help="size of window",type=int, default='5')

		args =  parser.parse_args()
		shot = args.shot
		#window = args.window
		#print("{}/{}".format(shot,window))
		print("{}".format(shot))
		pickle_name="rc03_{}.pickle".format(shot)	
		pickle_path = os.path.join(pickle_dir_path,pickle_name)
		print(pickle_path)
		draw(pickle_path)



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



if __name__ == "__main__":
	main(True,False,False)
