import yaml


# loading from a config file in read mode
def load_config(config_path=r"configs\default.yaml"):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config


# saving a config file in a particular location using write mode
def save_config(config, config_path=r"configs\default.yaml"):
    with open(config_path, "w") as f:
        yaml.dump(config, f)
