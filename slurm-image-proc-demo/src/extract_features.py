import os
import sys
import cv2
import numpy as np
from mpi4py import MPI

def extract_features(image_path):
    """提取图像的颜色直方图特征"""
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    # 计算HSV颜色直方图
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    return hist

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    if len(sys.argv) != 3:
        if rank == 0:
            print("用法: mpirun -np <进程数> python extract_features.py <输入目录> <输出文件>")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_file = sys.argv[2]
    
    # 获取所有图像文件
    if rank == 0:
        images = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        # 分发任务
        chunks = np.array_split(images, size)
    else:
        chunks = None
    
    # 分发任务到各进程
    local_images = comm.scatter(chunks, root=0)
    
    # 本地处理
    local_results = {}
    for img in local_images:
        img_path = os.path.join(input_dir, img)
        features = extract_features(img_path)
        if features is not None:
            local_results[img] = features.tolist()
    
    # 收集结果
    all_results = comm.gather(local_results, root=0)
    
    # 主进程保存结果
    if rank == 0:
        combined = {}
        for res in all_results:
            combined.update(res)
        
        # 保存为CSV
        with open(output_file, 'w') as f:
            f.write("filename,features\n")
            for img, feat in combined.items():
                feat_str = ','.join(map(str, feat))
                f.write(f"{img},{feat_str}\n")
        
        print(f"提取完成! 共处理 {len(combined)} 张图片")