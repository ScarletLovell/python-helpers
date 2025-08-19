import json
import typing
from dotty_dict import Dotty, dotty


class Config:
    """
    Configuration class for easily creating options
    
    Examples:
    ```
        config = Config()
        config.set_defaults({
            "app": {
                "test_thing": True,
                "another": 42
            },
            "basic_option": "basic"
        })
        config.load_and_put_defaults()
        config.push("app.test_thing", False)
        config.save()
        print(config.fetch("app.test_thing"))
        print(config.fetch("basic_option"))
    ```
    """

    # region Variables
    def set_location(self, location_local: str):
        """
        Set the location of the config file. (can be absolute or relative to current directory (`./`))

        Args:
            location_local (str): The new location of the config file.
        """
        self._location = location_local

    _location: str
    """
    The location of the config file.
    """

    _opt: Dotty = dotty()
    """
    The options of the config file; 
    Changed with `push()` and readable with `fetch()`.
    """

    def get_defaults(self) -> dict:
        """
        Get the defaults.

        Returns:
            dict: The defaults.
        """
        return self._defaults

    def set_defaults(self, d: dict):
        """
        Set the defaults to be loaded with `try_defaults`.

        Args:
            d (dict): The defaults to be loaded.
        """
        self._defaults = d

    _defaults: dict = {}
    """
    The defaults to be loaded with `try_defaults()`.
    """
    # endregion

    def __init__(self, location_local: str = "./config.json"):
        """
        Config initializer

        Args:
            location_local (str, optional): The location of the config file. Defaults to `"./config.json"`.
        """
        self._location = location_local
        self._opt = dotty()

    # region In-Line Options
    def push(self, object: str | tuple, value: typing.Any):
        """
        Pushes an object into the config; Does not autosave.

        Args:
            object (str): The object to write.
            value (any): The value to write.

        Examples:
            ```
            config.push("objectname", True)
            config.push(("dict", "objectname"), True)
            config.push(("dict1", "dict2", "anotherone", "objectname"), 42)
            config.push("dict1.dict2.anotherone.objectname", 42)
            ```
        """
        print(
            " - Saving Config Object {object} = {value}".format(
                object=object, value=value
            )
        )
        if isinstance(object, tuple):
            object = ".".join(object)
        self._opt[object] = value

    def fetch(self, object: str | tuple, default=None) -> typing.Any:
        """
        Reads (fetches) an objects' value in the config file.

        Args:
            object (str): The object to read.
            default (any, optional): The default value to return if the object is not found. Defaults to None.

        Returns:
            any: The value of the object.
        """
        if isinstance(object, tuple):
            object = ".".join(object)
        if default is None:
            default = self.get_defaults().get(object)
            return self._opt.get(object, default)
        return self._opt.get(object, default)

    # endregion

    # region Loading & Saving
    def load(self, overwrite_regardless: bool = False):
        """
        Loads the config file, without checking for defaults and without exception catching.
        This will create `YesNoDialog` if the config file is not found.

        Raises:
            FileNotFoundError: If the config file is not found.
        """
        with open(self._location, "r") as f:
            try:
                self._opt = dotty(json.load(f))
            except json.JSONDecodeError:
                if overwrite_regardless:
                    self._opt = dotty()
                    self.try_defaults()
                else:
                    from ui.dialog import show_dialog
                    show_dialog(
                        "Error in loading config!",
                        "There was an error loading the current config, do you want to overwrite it?",
                        lambda x: self.save() if x else None
                    )

    def load_and_put_defaults(self):
        """
        Loads the config file and checks for defaults. (via `try_defaults()`)

        Does not raise an exception, but catches exception `FileNotFoundError`
        """
        try:
            print("Loading config file...")
            self.load()
            print("Config file loaded; checking for defaults...")
            written = self.try_defaults(raise_exception=False)
            if written > 0:
                print("Wrote " + str(written) + " defaults.")
            else:
                print("No defaults written.")
        except FileNotFoundError:
            self.save()

    def try_defaults(self, raise_exception: bool = True) -> int:
        """
        Set defaults with `set_defaults`, and this will attempt to load them.
        Does not overwrite existing values.

        Args:
            raise_exception (bool, optional): If True, will raise an exception if defaults are empty. Defaults to True.

        Raises:
            Exception: If the defaults are empty. (`raise_exception` must be True)

        Returns:
            int: The number of defaults that were written.
        """
        changed_count = 0
        # check if defaults are empty, if they are then raise exception
        if len(self._defaults) < 1:
            if raise_exception:
                raise Exception("Attempted to load defaults but defaults are empty.")
            return changed_count
        should_save = False
        for key, value in self._defaults.items():
            if key not in self._opt:
                self._opt[key] = value
                should_save = True
                changed_count += 1
        if should_save:
            self.save()
        return changed_count

    def save(self):
        """
        Saves the current configuration to the file.
        """

        with open(self._location, "w") as f:
            json.dump(self._opt.to_dict(), f, indent=4)

    # endregion
