import os
import sys
from PIL import Image
from utils import *
from thread_pool import gthread_pool
def convert_image(input_path,format = 'png'):
    try:
        img = Image.open(input_path)
        new_file = change_file_extension(input_path,format)
        out_path = replace_up_dir(new_file,format)
        img.save(out_path, format=format)
        print("convert file:",out_path)
        return True
    except Exception as e:
        print(f"转换失败: {e}")
        return False
    
def convert_images(images):
    for image in images:
        convert_image(image)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python convert_format.py <文件目录>")
        sys.exit(1)
    input_dir = sys.argv[1]
    images = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    max_worker = gthread_pool.max_workers
    images_batchs = array_split(images,max_worker)
    args = [ [os.path.join(input_dir, image) for image in batch] for batch in images_batchs]
    gthread_pool.submit_batch(convert_images,args)
