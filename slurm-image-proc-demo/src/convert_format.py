import os
import sys
from PIL import Image
from utils import *

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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python convert_format.py <文件目录>")
        sys.exit(1)
    input_dir = sys.argv[1]
    images = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    for filename in images:
        input_path = os.path.join(input_dir, filename)
        convert_image(input_path)
