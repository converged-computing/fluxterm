import yaml


def read_yaml(filename):
    """
    Read yaml from file
    """
    with open(filename, "r") as fd:
        data = yaml.safe_load(fd)
    return data
