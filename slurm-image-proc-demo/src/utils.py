import os
def replace_up_dir(path, new_dir):
    parts = path.split('/')
    if len(parts) >= 3:  # 确保路径包含根目录、两级目录和文件名
        parts[-2] = new_dir  # 替换第二级目录（索引为2的部分）
    return '/'.join(parts)
def change_file_extension(file_path, new_extension):
    # 确保新扩展名以点号开头
    if not new_extension.startswith('.'):
        new_extension = '.' + new_extension
    # 分离路径和文件名
    directory = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    # 分离文件名和原扩展名
    base_name, _ = os.path.splitext(filename)
    # 组合新文件名
    new_filename = base_name + new_extension
    # 组合新路径
    new_path = os.path.join(directory, new_filename)
    return new_path
def add_str_to_filename(path, string):
    # 找到最后一个斜杠的位置
    last_slash_index = path.rfind('/')
    
    # 分离目录路径和文件名
    if last_slash_index != -1:
        directory = path[:last_slash_index + 1]  # 包含结尾的斜杠
        filename = path[last_slash_index + 1:]
    else:
        directory = ""  # 如果没有斜杠，整个字符串视为文件名
        filename = path
    
    # 找到最后一个点（扩展名分隔符）
    last_dot_index = filename.rfind('.')
    
    # 分离主文件名和扩展名
    if last_dot_index != -1:
        main_name = filename[:last_dot_index]
        extension = filename[last_dot_index:]  # 包含点
    else:
        main_name = filename
        extension = ""
    
    # 在文件名后添加后缀并重组路径
    new_filename = f"{main_name}{string}{extension}"
    return directory + new_filename