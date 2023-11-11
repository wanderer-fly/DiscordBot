import os
import yaml

def read_config():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.yaml')
    with open(config_path, 'r') as config_file:
        config = yaml.load(config_file, Loader = yaml.FullLoader)
    return config
