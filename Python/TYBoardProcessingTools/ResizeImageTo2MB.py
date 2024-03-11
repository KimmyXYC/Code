import os


def increase_file_size(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                print(file_path, file_size)
                if file_size < 2 * 1024 * 1024:  # 2MB
                    with open(file_path, 'ab') as f:
                        f.write(b'\0' * (2 * 1024 * 1024 - file_size))


directory = '/path/to/your/directory'
increase_file_size(directory)
