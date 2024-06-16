import os.path
import yaml
import logging
import logging.config


def setup_logging(default_level=logging.INFO):
    path = os.path.join(os.getcwd(), "logging.yml")
    if os.path.exists(path):
        with open(path, "rt") as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
            except Exception as e:
                print(e)
                print("Error in Logging Configuration. Using default configs")
                logging.basicConfig(level=default_level)
            finally:
                return logging
    else:
        logging.basicConfig(level=default_level)
        print("Failed to load configuration file. Using default configs")
        return logging
