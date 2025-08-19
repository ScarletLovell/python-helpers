# Simple Config Manager

A straightforward Python class for managing application settings using a JSON file.

This tool helps you easily save, load, and manage configuration options for your projects without any complex setup.

## Features

*   **Easy to Use**: A simple and clean API for managing settings.
*   **JSON Backend**: Stores configurations in a human-readable `.json` file.
*   **Default Values**: Automatically populates the configuration file with default values if it's missing or empty.
*   **Dot Notation**: Access nested settings easily (e.g., `app.window.width`).
*   **Single File**: Just drop `config.py` into your project and you're ready to go.

## How to Use

### 1. Add to Your Project

Copy the `core/config.py` file into your project directory.

### 2. Example Usage

Here’s a quick guide on how to use the `Config` class.

```python
# 1. Import the class from the file
from core.config import Config

# 2. Create a new config object.
# By default, it will look for a file named "config.json" in the current directory.
config = Config()

# You can also specify a custom path:
config = Config("./settings/my_app_config.json")
# or absolute paths (Linux & Windows are supported, this is just an example)
config = Config("C:\Users\test\config.json")

# 3. Set up your default settings.
# These are used if the config file is new or a setting is missing.
config.set_defaults({
    "app": {
        "dark_mode": True,
        "username": "Guest"
    },
    "version": "1.0"
})

# 4. Load the config file.
# If "config.json" doesn't exist, it will be created with your defaults.
# If it already exists, it will load the settings and add any missing defaults.
config.load_and_put_defaults()

# 5. Read (fetch) a setting
# Use "dot notation" to get values, even nested ones.
is_dark_mode = config.fetch("app.dark_mode")
print(f"Dark mode is: {is_dark_mode}")

username = config.fetch("app.username")
print(f"Current user is: {username}")

# 6. Change (push) a setting
# This updates the setting in memory, but doesn't save it to the file yet.
config.push("app.username", "Gemini")
print("Username has been updated in memory.")

# 7. Save your changes
# This writes all the current settings to the "config.json" file.
config.save()
print("Configuration saved to file!")
```

After running this code, your `config.json` file will look like this:

```json
{
    "app": {
        "dark_mode": true,
        "username": "Gemini"
    },
    "version": "1.0"
}
```
