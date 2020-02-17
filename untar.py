import os
import numpy as np
import multiprocessing as mp
import tarfile, sys 

src_dir='../zip'
dst_dir='../dataset'

def untar_func(src_path, dst_path):
	print("untar {} => {}\n".format(src_path,dst_path))
	untar_inst = tarfile.open(src_path)
	untar_inst.extractall(dst_path)
	untar_inst.close()

pool = mp.Pool(mp.cpu_count())
file_name_lists = np.sort(os.listdir(src_dir))
print("file_lists = {}".format(file_name_lists))
tar_path_lists = []
for file_name in file_name_lists:
	if file_name.lower().endswith("tar.gz"):
		file_path= os.path.join(src_dir,file_name)
		if os.path.exists(file_path):
			tar_path_lists.append(file_path)
			print("append file name = {}".format(file_path))

results = [pool.apply_async(untar_func, args=(tar_path,dst_dir))for tar_path in tar_path_lists]
pool.close()
pool.join()



