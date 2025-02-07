"""
loadcfg: A configuration helper library.

This library provides functions to load configuration files in JSON, YAML, TOML,
and INI formats into a configuration object that supports attribute (dot) access.
It also supplies a base Template class to create configuration schemas,
validate loaded configurations, and generate example configuration files.
"""

import configparser
import json
from io import StringIO

import toml
import yaml

__all__ = [
    "Config",
    "LoadJson",
    "LoadYaml",
    "LoadToml",
    "LoadIni",
    "Template",
    "ConfigValidationError",
]


class Config(dict):
    """Configuration object that supports attribute access to dictionary keys.

    This class recursively converts dictionaries into Config objects, allowing
    dot notation access to configuration values.

    Example:
        config = Config({'name': 'Alice', 'age': 30})
        print(config.name)  # Output: Alice
    """

    def __init__(self, data):
        """Initialize the Config object with a dictionary.

        Args:
            data (dict): Dictionary representing configuration data.

        Raises:
            ValueError: If the provided data is not a dictionary.
        """
        super().__init__()
        if not isinstance(data, dict):
            raise ValueError("Config data must be a dictionary")
        for key, value in data.items():
            self[key] = self._convert_value(value)

    def _convert_value(self, value):
        """Recursively convert dictionaries (and lists containing dicts)
        into Config objects.

        Args:
            value: The value to convert.

        Returns:
            The converted value.
        """
        if isinstance(value, dict):
            return Config(value)
        elif isinstance(value, list):
            return [self._convert_value(item) for item in value]
        else:
            return value

    def __getattr__(self, item):
        """Allow attribute access to dictionary keys.

        Args:
            item (str): The key name.

        Returns:
            The value associated with the key.

        Raises:
            AttributeError: If the key is not found.
        """
        try:
            return self[item]
        except KeyError:
            raise AttributeError(f"'Config' object has no attribute '{item}'")

    def __setattr__(self, key, value):
        """Allow setting values using attribute syntax.

        Args:
            key (str): The key name.
            value: The value to set.
        """
        self[key] = value

    def validate(self, template):
        """Validate the configuration against a given template.

        This method delegates to the template's class method.

        Args:
            template (Type[Template]): The Template class to validate against.

        Raises:
            ConfigValidationError: If the configuration does not match the template.
        """
        template.validate(self)


def LoadJson(file_path: str) -> Config:
    """Load a JSON configuration file and return a Config object.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        Config: The loaded configuration as a Config object.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return Config(data)


def LoadYaml(file_path: str) -> Config:
    """Load a YAML configuration file and return a Config object.

    Args:
        file_path (str): Path to the YAML file.

    Returns:
        Config: The loaded configuration as a Config object.

    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If the file is not valid YAML.
        ValueError: If the YAML file does not contain a top-level dictionary.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError("YAML file must contain a top-level dictionary")
    return Config(data)


def LoadToml(file_path: str) -> Config:
    """Load a TOML configuration file and return a Config object.

    Args:
        file_path (str): Path to the TOML file.

    Returns:
        Config: The loaded configuration as a Config object.

    Raises:
        FileNotFoundError: If the file does not exist.
        toml.TomlDecodeError: If the file is not valid TOML.
        ValueError: If the TOML file does not contain a top-level table.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = toml.load(f)
    if not isinstance(data, dict):
        raise ValueError("TOML file must contain a top-level table")
    return Config(data)


def LoadIni(file_path: str) -> Config:
    """Load an INI configuration file and return a Config object.

    Args:
        file_path (str): Path to the INI file.

    Returns:
        Config: The loaded configuration as a Config object.

    Raises:
        FileNotFoundError: If the file does not exist.
        configparser.Error: If the file is not a valid INI file.
    """
    parser = configparser.ConfigParser()
    parser.read(file_path, encoding="utf-8")
    data = {}
    # Process each section into a nested dictionary.
    for section in parser.sections():
        data[section] = dict(parser.items(section))
    # Merge the DEFAULT values into the top-level dictionary.
    if parser.defaults():
        data.update(parser.defaults())
    return Config(data)


class ConfigValidationError(Exception):
    """Exception raised for errors in configuration validation.

    Attributes:
        message (str): Explanation of the error.
    """

    def __init__(self, message):
        """Initialize ConfigValidationError with an error message.

        Args:
            message (str): The error message.
        """
        super().__init__(message)
        self.message = message


def _dict_to_ini(data: dict) -> str:
    """Convert a dictionary into an INI-formatted string.

    Args:
        data (dict): The dictionary to convert.

    Returns:
        str: The resulting INI-formatted string.
    """
    config = configparser.ConfigParser()
    default_section = {}
    for key, value in data.items():
        if isinstance(value, dict):
            # Each nested dictionary becomes its own section.
            config[key] = {subkey: str(subvalue) for subkey, subvalue in value.items()}
        else:
            default_section[key] = str(value)
    if default_section:
        config["DEFAULT"] = default_section
    with StringIO() as stream:
        config.write(stream)
        return stream.getvalue()


class Template:
    """Base class for configuration templates.

    Subclass this to define a configuration schema. Use type annotations to
    specify the expected fields and their types.

    Example:
        class ProgramConfig(Template):
            name: str
            age: int

        # Validate a loaded config:
        config = LoadYaml("config.yaml")
        ProgramConfig.validate(config)

        # Generate an example configuration (JSON format by default):
        example_config = ProgramConfig.generate(fmt="json")
        print(example_config)
    """

    def __init_subclass__(cls):
        """Automatically collect field definitions from type annotations.

        If no type annotations are provided, attempts to use class attributes that do
        not start with an underscore.
        """
        super().__init_subclass__()
        if hasattr(cls, "__annotations__") and cls.__annotations__:
            cls._fields = cls.__annotations__
        else:
            cls._fields = {
                k: type(v) for k, v in cls.__dict__.items() if not k.startswith("_") and not callable(v)
            }

    @classmethod
    def validate(cls, config: Config):
        """Validate that the given configuration matches the template.

        This method checks that all required fields are present in the config and
        that the types of the provided values match the expected types. If a field’s
        expected type is a subclass of Template, the validation is performed recursively.

        Args:
            config (Config): The configuration object to validate.

        Raises:
            ConfigValidationError: If a required field is missing or if a field has an
                                   incorrect type.
        """
        for field, expected_type in cls._fields.items():
            if not hasattr(config, field):
                raise ConfigValidationError(f"Missing required field: '{field}'")
            value = getattr(config, field)
            if isinstance(expected_type, type) and issubclass(expected_type, Template):
                try:
                    expected_type.validate(value)
                except ConfigValidationError as e:
                    raise ConfigValidationError(f"In field '{field}': {str(e)}")
            else:
                if not isinstance(value, expected_type):
                    raise ConfigValidationError(
                        f"Field '{field}' expected type '{expected_type.__name__}', "
                        f"got '{type(value).__name__}'"
                    )

    @classmethod
    def generate(cls, fmt: str = "json") -> str:
        """Generate an example configuration based on the template.

        The example is generated using default values for basic types. For instance,
        int becomes 0, str becomes "example", and bool becomes False. For nested templates,
        the generation is done recursively.

        Args:
            fmt (str): Format of the output. Supported values are "json", "yaml" (or "yml"),
                       "toml", and "ini". Defaults to "json".

        Returns:
            str: A string representing the example configuration.

        Raises:
            ValueError: If the specified format is unsupported.
        """
        example_dict = cls._generate_example_dict()
        fmt_lower = fmt.lower()
        if fmt_lower == "json":
            return json.dumps(example_dict, indent=4)
        elif fmt_lower in ("yaml", "yml"):
            return yaml.dump(example_dict, default_flow_style=False)
        elif fmt_lower == "toml":
            return toml.dumps(example_dict)
        elif fmt_lower == "ini":
            return _dict_to_ini(example_dict)
        else:
            raise ValueError("Unsupported format. Use 'json', 'yaml', 'toml', or 'ini'.")

    @classmethod
    def _generate_example_dict(cls) -> dict:
        """Helper method to generate a dictionary with example values based on the template.

        Returns:
            dict: Dictionary containing example configuration values.
        """
        example = {}
        for field, expected_type in cls._fields.items():
            if isinstance(expected_type, type) and issubclass(expected_type, Template):
                example[field] = expected_type._generate_example_dict()
            else:
                example[field] = _get_example_value(expected_type)
        return example


def _get_example_value(expected_type):
    """Return an example value for a given expected type.

    Args:
        expected_type (type): The expected type.

    Returns:
        An example value corresponding to the type.
    """
    if expected_type is int:
        return 0
    elif expected_type is float:
        return 0.0
    elif expected_type is str:
        return "example"
    elif expected_type is bool:
        return False
    elif expected_type is list:
        return []
    elif expected_type is dict:
        return {}
    else:
        return None
