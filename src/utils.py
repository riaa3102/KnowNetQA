import logging
import yaml
from box import Box
from pathlib import Path
from src import dirs


def setup_logging():
    # Define the format for the logging
    log_format = '%(asctime)s - %(levelname)s - %(message)s'

    # Create a logger object
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create a file handler to write logs to a file
    log_file_path = dirs.LOGS_DIR / 'logs.txt'
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)  # Set the logging level for the file handler
    file_handler.setFormatter(logging.Formatter(log_format))

    # Create a console handler to output logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format))

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def load_config(config_file="config.yaml"):
    """Load the YAML configuration file."""
    config_path = Path(__file__).parent / config_file
    with config_path.open('r') as file:
        config = yaml.safe_load(file)
    return Box(config)


# Setup logger
logger = setup_logging()

# Load config
config = load_config()
