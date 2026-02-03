import os
import numpy as np
import zipfile
from pathlib import Path

import h5py
from PIL import Image
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import shutil

def list_files_in_zip(zip_path):
    file_list = []
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        file_list = zip_ref.namelist()
    return file_list

def list_zip_files_in_dir(dir_path):
    d_path = Path(dir_path)
    # file_list = [f for f in d_path.iterdir() if f.is_file()]
    zip_list = list(d_path.glob('*.zip'))
    return zip_list

def images_to_hdf5(image_path, output_path, img_size=(224, 224),img_cut_th = 2):
    image_paths = list(sorted(image_path.glob("*.bmp"))) # 혹은 *.png
    frame_numbers = [int(p.stem.split('-')[-1]) for p in image_paths]
    num_images = len(image_paths)
    shot_number = image_path.name.split('_')[0]
    # print(f"shot number: {shot_number}, Number of Image: {num_images}")
    patch_size = 80
   
    # target_h = img_size[1]
    # target_w = img_size[0]

    # cimg_size = (crop_width, img_size[1])

    valid_paths = []
    valid_frame_numbers = []
    resize_crop_width = 0
    for path, frame_num in zip(image_paths, frame_numbers):
        # print(f"  Image path: {path}, Frame number: {frame_num}")
        with Image.open(path) as img:
            org_img_size = img.size
            org_crop_width = org_img_size[0] - 2*patch_size
            org_right = org_img_size[0] - patch_size

            resize_crop_width  = org_crop_width*img_size[0]//org_img_size[1]
            cropped_img = img.crop((patch_size, 0, org_right, org_img_size[1]))
            resize_cropped_size = (resize_crop_width, img_size[1])
            gimg = cropped_img.resize(resize_cropped_size).convert('L')

            g_avg = np.mean(np.array(gimg))
            if g_avg >= img_cut_th:
                valid_paths.append(path)
                valid_frame_numbers.append(frame_num)

            # print(f"imag.size = {img.size}, org_crop_width = {org_crop_width}, resize_crop_width = {resize_crop_width}")
            # else:
            #     print(f"    Skipped due to low brightness (Avg: {g_avg:.2f})")
    num_valid = len(valid_paths)
    if num_valid == 0:
        print(f"  No valid images found for shot {shot_number}. Skipping HDF5 creation.")
        return 0

    
    
    # 1. HDF5 파일 생성
    with h5py.File(output_path, 'w') as h5f:
        # 2. 데이터를 담을 빈 공간(Dataset) 미리 생성
        # (개수, 높이, 너비, 채널) 순서
        image_dset = h5f.create_dataset(f"tv01_{shot_number}", 
                                  shape=(num_valid,img_size[1], resize_crop_width, 3), 
                                  dtype=np.uint8,
                                  compression="gzip") # 용량 압축 옵션
        frame_dset = h5f.create_dataset("frame_numbers", 
                                        shape=(num_valid,), 
                                        dtype=np.int32)
        
        # 3. 이미지 읽어서 HDF5에 채우기
        for i, (path, frame_num) in enumerate(tqdm(zip(valid_paths, valid_frame_numbers), total=num_valid,desc=f"Convert to HDF5 for shot {shot_number}")):
            fram_num = path.stem.split('-')[-1]
            # print(f"  Frame number: {fram_num}")
            img = Image.open(path).convert('RGB')
            org_img_size = img.size
            org_crop_width = org_img_size[0]-2*patch_size
            org_right = org_img_size[0] - patch_size
            resize_crop_width  = org_crop_width*img_size[0]//org_img_size[1]
            cropped_img = img.crop((patch_size, 0, org_right, org_img_size[1]))
            resize_cropped_size = (resize_crop_width, img_size[1])


            crop_resize_img = cropped_img.resize(resize_cropped_size) # 크기 통일 필수
           
            image_dset[i] = np.array(crop_resize_img)
            frame_dset[i] = frame_num
            
    # print(f"Save complete: {output_path}")
    return num_valid

def process_shot(zip_path):
    # print(f"  {zip_path.absolute()}") 
    try:
        extract_to = zip_path.parent / zip_path.stem
        shot_number = extract_to.name.split('_')[0]
        output_hdf5_path = extract_to.parent / f"{zip_path.stem}.h5"
        if output_hdf5_path.exists():
            return f"Shot {shot_number}: Already exists." 
        Path(extract_to).mkdir( exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            # print(f"all files are extracted to '{extract_to}'.")
        
        num_valid = images_to_hdf5(extract_to, output_hdf5_path, img_size=(224, 224), img_cut_th=2)
        if extract_to.exists():
            shutil.rmtree(extract_to)
        return f"Shot {shot_number}: {num_valid} valid images processed."
    except Exception as e:
        if extract_to.exists():
            shutil.rmtree(extract_to)
        return f"Shot {zip_path.name} Error: {str(e)}"
    
if __name__ == "__main__":
    years = ["2025C18"]

    base_dir_path = "/Users/giilkwon/WorkSpace/KSTAR_TV_DATASET/tv_efit"
    dataset_dir_paths_t = [os.path.join(base_dir_path,year) for year in years]
    dataset_dir_paths = [os.path.join(d, "TV01") for d in dataset_dir_paths_t]
    # print(f"dataset dirs: {dataset_dir_paths}")

    num_cores = int(cpu_count() * 0.8)
    print(f"Starting parallel processing with {num_cores} cores...")

    for d_path in dataset_dir_paths:
        zip_file_list = list_zip_files_in_dir(d_path)

        with Pool(num_cores) as pool:
            results = list(tqdm(pool.imap(process_shot,zip_file_list), total=len(zip_file_list), desc="Processing Shots"))

    # for d_path in dataset_dir_paths:
    #     zip_file_list = list_zip_files_in_dir(d_path)
    #     for zip_path in zip_file_list:
            