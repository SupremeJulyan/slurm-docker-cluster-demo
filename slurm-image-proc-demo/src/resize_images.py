import os
import sys
from PIL import Image
import numpy as np
from utils import *

def resize_image(input_path, size=(512, 512)):
    try:
        img = Image.open(input_path)
        img = img.resize(size)
        new_file = add_str_to_filename(input_path,f"_{size[0]}x{size[1]}")
        out_path = replace_up_dir(new_file,"resize")
        img.save(out_path)
        print("resize file:",out_path)
        return True
    except Exception as e:
        print(f"缩放失败: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python resize_images.py <输入目录> <尺寸>")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    size = tuple(map(int, sys.argv[2].split('x')))

    
    # 获取文件列表
    images = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    # 通过环境变量获取任务ID
    task_id = int(os.getenv('SLURM_ARRAY_TASK_ID', 0))
    total_tasks = int(os.getenv('SLURM_ARRAY_TASK_COUNT', 1))
    chunks = np.array_split(images,total_tasks)
    images_chunks = [list(c) for c in chunks]
    print("task_id,total_tasks:",task_id,total_tasks)
    # 分配任务
    for filename in  images_chunks[task_id]:
        input_path = os.path.join(input_dir, filename)
        if resize_image(input_path, size):
            print(f"缩放成功: {filename}")