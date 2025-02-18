import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "work_hours": {
        "Monday": {"start": 9, "end": 18},
        "Tuesday": {"start": 9, "end": 18},
        "Wednesday": {"start": 9, "end": 18},
        "Thursday": {"start": 9, "end": 18},
        "Friday": {"start": 9, "end": 18},
        "Saturday": {"start": None, "end": None},
        "Sunday": {"start": None, "end": None}
    },
    "max_concentration_hours": 2.0,
    "min_break_minutes": 10
}

def load_config():
    """Loads the user configuration from the file. If the file does not exist, saves the default configuration."""
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
    
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(config):
    """Saves the user configuration to the file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def update_config(key, value):
    """Updates a specific key in the configuration file."""
    config = load_config()
    config[key] = value
    save_config(config)
