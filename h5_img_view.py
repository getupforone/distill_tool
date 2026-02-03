import h5py
import tkinter as tk
from tkinter import filedialog
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class H5AdvancedViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("KSTAR HDF5 Analysis Viewer")
        self.root.geometry("1100x850")

        self.h5_file = None
        self.dset_name = None
        self.image_data = None
        self.frame_numbers = None
        self.current_idx = 0

        # --- 상단 컨트롤 영역 ---
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.btn_load = tk.Button(self.top_frame, text="HDF5 파일 불러오기", command=self.load_file, width=20)
        self.btn_load.pack(side=tk.LEFT, padx=10)

        self.info_label = tk.Label(self.top_frame, text="파일을 불러와주세요.", font=("Arial", 11, "bold"))
        self.info_label.pack(side=tk.LEFT, padx=20)

        # --- 하단 컨트롤 영역 (이전/다음 버튼 + 슬라이더) ---
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        self.btn_prev = tk.Button(self.bottom_frame, text="◀ 이전", command=self.prev_frame, width=10)
        self.btn_prev.pack(side=tk.LEFT, padx=20)

        self.slider = tk.Scale(self.bottom_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.on_slider_move)
        self.slider.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.btn_next = tk.Button(self.bottom_frame, text="다음 ▶", command=self.next_frame, width=10)
        self.btn_next.pack(side=tk.LEFT, padx=20)

        # --- 메인 컨텐츠 영역 (이미지 + 히스토그램) ---
        self.display_frame = tk.Frame(root)
        self.display_frame.pack(fill=tk.BOTH, expand=True)


        # Matplotlib Figure 구성 (1행 2열)
        self.fig, (self.ax_img, self.ax_hist) = plt.subplots(1, 2, figsize=(10, 5), gridspec_kw={'width_ratios': [1.5, 1]})
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.display_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)



    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("HDF5 files", "*.h5 *.hdf5")])
        if not file_path: return

        self.h5_file = h5py.File(file_path, 'r')
        self.dset_name = [k for k in self.h5_file.keys() if k.startswith('tv01')][0]
        self.image_data = self.h5_file[self.dset_name]
        self.frame_numbers = self.h5_file['frame_numbers']

        num_frames = len(self.image_data)
        self.slider.config(from_=0, to=num_frames - 1)
        self.current_idx = 0
        self.update_display()

    def update_display(self):
        if self.image_data is None: return

        idx = self.current_idx
        img = self.image_data[idx]
        frame_val = self.frame_numbers[idx]
        shot_num = self.dset_name.split('_')[-1]

        # 1. 정보 업데이트
        self.info_label.config(text=f"Shot: {shot_num} | Frame: {frame_val} (Index: {idx})")
        self.slider.set(idx)

        # 2. 이미지 그리기
        self.ax_img.clear()
        self.ax_img.imshow(img)
        self.ax_img.set_title(f"Image View (Shot {shot_num})")
        self.ax_img.axis('off')

        # 3. 히스토그램 그리기
        self.ax_hist.clear()
        # 이미지가 RGB일 수 있으므로 밝기(Grayscale) 계산 후 히스토그램 생성
        if len(img.shape) == 3:
            gray = np.dot(img[...,:3], [0.2989, 0.5870, 0.1140])
        else:
            gray = img
        g_avg = np.mean(gray)

            
        self.ax_hist.hist(gray.ravel(), bins=64, range=(0, 255), color='gray', alpha=0.7)
        self.ax_hist.set_title(f"Brightness Histogram (Avg: {g_avg:.2f})")
        self.ax_hist.set_xlabel("Pixel Intensity")
        self.ax_hist.set_ylabel("Frequency")
        self.ax_hist.set_xlim(0, 255)

        self.canvas.draw()

    def on_slider_move(self, val):
        new_idx = int(val)
        if new_idx != self.current_idx:
            self.current_idx = new_idx
            self.update_display()

    def next_frame(self):
        if self.image_data and self.current_idx < len(self.image_data) - 1:
            self.current_idx += 1
            self.update_display()

    def prev_frame(self):
        if self.image_data and self.current_idx > 0:
            self.current_idx -= 1
            self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = H5AdvancedViewer(root)
    root.mainloop()