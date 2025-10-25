from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import random
import os
import sys

def generate_image_variations(base_image_path, n, output_dir="data/source"):
    """
    以基准图片生成n张变体图片
    
    参数:
    base_image_path (str): 原始图片路径
    n (int): 需要生成的图片数量
    output_dir (str): 输出目录（默认为"output"）
    
    返回:
    list: 生成的图片路径列表
    """
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 打开原始图片
    original_img = Image.open(base_image_path)
    base_name = os.path.basename(base_image_path)
    name, ext = os.path.splitext(base_name)
    
    generated_paths = []
    
    for i in range(n):
        # 创建原始图片的副本
        img = original_img.copy()
        
        # 随机选择一种变换方式
        transform_type = random.choice([
            'rotate', 'flip', 'color', 'contrast', 
            'brightness', 'blur', 'crop', 'noise'
        ])
        
        # 应用变换
        if transform_type == 'rotate':
            angle = random.uniform(-30, 30)
            img = img.rotate(angle, expand=True)
            img = img.resize(original_img.size)  # 保持原始尺寸
            
        elif transform_type == 'flip':
            if random.choice([True, False]):
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            else:
                img = img.transpose(Image.FLIP_TOP_BOTTOM)
                
        elif transform_type == 'color':
            enhancer = ImageEnhance.Color(img)
            factor = random.uniform(0.5, 1.5)
            img = enhancer.enhance(factor)
            
        elif transform_type == 'contrast':
            enhancer = ImageEnhance.Contrast(img)
            factor = random.uniform(0.5, 1.5)
            img = enhancer.enhance(factor)
            
        elif transform_type == 'brightness':
            enhancer = ImageEnhance.Brightness(img)
            factor = random.uniform(0.7, 1.3)
            img = enhancer.enhance(factor)
            
        elif transform_type == 'blur':
            radius = random.uniform(0.5, 2.0)
            img = img.filter(ImageFilter.GaussianBlur(radius))
            
        elif transform_type == 'crop':
            # 随机裁剪并缩放回原始尺寸
            width, height = img.size
            crop_width = random.randint(int(width*0.7), width)
            crop_height = random.randint(int(height*0.7), height)
            left = random.randint(0, width - crop_width)
            top = random.randint(0, height - crop_height)
            img = img.crop((left, top, left+crop_width, top+crop_height))
            img = img.resize(original_img.size)
            
        elif transform_type == 'noise':
            # 添加随机噪声
            np_img = np.array(img)
            noise = np.random.randint(-30, 30, np_img.shape, dtype=np.int32)
            np_img = np.clip(np_img + noise, 0, 255).astype(np.uint8)
            img = Image.fromarray(np_img)
        
        # 保存生成的图片
        output_path = os.path.join(output_dir, f"{name}_variant_{i+1}{ext}")
        img.save(output_path)
        generated_paths.append(output_path)
    
    return generated_paths

# 使用示例
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python generate_images.py <图片路径> <生成图片个数>")
        sys.exit(1)
    # 生成5张基于"example.jpg"的变体图片
    variations = generate_image_variations(sys.argv[1], int(sys.argv[2]))
    print("生成的图片路径:")
    for path in variations:
        print(path)