import yaml


def main():
    block_type = (read_yaml_file()["blockType"] + 1) % 2
    write_yaml_file(block_type, "blockType")



def read_yaml_file():
    with open("config.yml", 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        return data


def write_yaml_file(value, parameter):
    with open("config.yml", 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        data[parameter] = value

    with open("config.yml", 'w', encoding='utf-8') as file:
        yaml.dump(data, file, allow_unicode=True)

if __name__ == '__main__':
    main()
