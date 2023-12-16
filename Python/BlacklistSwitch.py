import ruamel.yaml
import sys


def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == "1":
            block_type = 1
            write_yaml_file(block_type, "blockType")
        elif sys.argv[1] == "0":
            block_type = 0
            write_yaml_file(block_type, "blockType")


def write_yaml_file(value, parameter):
    yaml = ruamel.yaml.YAML()
    with open("config.yml", 'r', encoding='utf-8') as file:
        data = yaml.load(file)
    data[parameter] = value
    with open("config.yml", 'w', encoding='utf-8') as file:
        yaml.dump(data, file)

if __name__ == '__main__':
    main()
