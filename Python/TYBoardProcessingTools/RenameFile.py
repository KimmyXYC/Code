import os

INFO = [
    "合理膳食包含五大类营养素：碳水化合物、蛋白质、脂肪、维生素和矿物质。",
    # ... 其他元素
    "饮食宜清淡，减少胃肠道负担。",
    "合理膳食有助于改善心肺功能。",
]


def rename_files_with_info(directory, info):
    files = os.listdir(directory)
    for i, file_name in enumerate(files, start=1):
        base_name, extension = os.path.splitext(file_name)
        new_name = f"{i}.{info[i - 1]}{extension}"
        os.rename(os.path.join(directory, file_name), os.path.join(directory, new_name))
        print(f"Renamed {file_name} to {new_name}")


def write_info_to_txt(info, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for i, description in enumerate(info, start=1):
            file.write(f"{i}.{description}\n")
        print(f"INFO 内容已写入到 {file_path}")


# 请将 'directory' 替换为你的目录路径
directory = '/path/to/your/directory'
file_path = '/path/to/your/info.txt'
rename_files_with_info(directory, INFO)
write_info_to_txt(INFO, file_path)
