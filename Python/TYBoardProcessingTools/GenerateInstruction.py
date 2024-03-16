import os

# 指定要遍历的目录
target_directory = '/path/to/your/directory'

# 指定输出txt文件的路径和名称
output_file_path = '/path/to/output.txt'

# 遍历目录并提取、排序文件名
file_info_list = []
for filename in os.listdir(target_directory):
    if os.path.isfile(os.path.join(target_directory, filename)):
        file_parts = filename.split('.')
        if len(file_parts) > 2:
            number_and_description = int(file_parts[0]), '.'.join(file_parts[1:3])[:-4]  # 去掉格式部分
            file_info_list.append(number_and_description)

# 根据编号排序
file_info_list.sort(key=lambda x: x[0])

# 将排序后的信息写入txt文件
with open(output_file_path, 'w') as output_file:
    for number, description in file_info_list:
        output_line = f'{number}.{description}\n'
        output_file.write(output_line)

# 完成后关闭输出文件
output_file.close()
