import os
import numpy as np
import multiprocessing as mp
import zipfile

src_dir='/data2/TV'
dst_dir='/data3/KSTAR_TV_DATASET/bmp'

def unzip_func(src_path, dst_path):
	print("unzip {} => {}\n".format(src_path,dst_path))
	unzip_inst = zipfile.ZipFile(src_path)
	unzip_inst.extractall(dst_path)
	unzip_inst.close()

pool = mp.Pool(mp.cpu_count())
file_name_lists = np.sort(os.listdir(src_dir))
print("file_lists = {}".format(file_name_lists))
zip_path_lists = []
for file_name in file_name_lists:
	if file_name.lower().endswith("zip"):
		file_path= os.path.join(src_dir,file_name)
		if os.path.exists(file_path):
			zip_path_lists.append(file_path)
			print("append file name = {}".format(file_path))

results = [pool.apply_async(unzip_func, args=(zip_path,dst_dir))for zip_path in zip_path_lists]
pool.close()
pool.join()



