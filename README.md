# loadcfg

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/danielkorkin/loadcfg/test.yml?label=testing)
[![PyPI - Version](https://img.shields.io/pypi/v/loadcfg)](https://pypi.org/project/loadcfg)  
[![Codecov](https://img.shields.io/codecov/c/github/danielkorkin/loadcfg)](https://app.codecov.io/gh/danielkorkin/loadcfg/)  
[![Read the Docs](https://img.shields.io/readthedocs/loadcfg)](https://loadcfg.readthedocs.io)  
[![PyPI - License](https://img.shields.io/pypi/l/loadcfg)](https://pypi.org/project/loadcfg)  
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/loadcfg)](https://pypi.org/project/loadcfg)  
[![GitHub last commit](https://img.shields.io/github/last-commit/danielkorkin/loadcfg)](https://github.com/danielkorkin/loadcfg)

**loadcfg** is a lightweight Python library that makes it easy to load configuration files in JSON and YAML formats with convenient dot-access to configuration values.

- **Install with:** `pip install loadcfg`
- **License:** MIT License
- **Maintained by:** Daniel Korkin (<daniel.d.korkin@gmail.com>)
- **Library Purpose:** Easily load and validate configuration files (JSON and YAML)
- **Documentation:** [loadcfg.readthedocs.io](https://loadcfg.readthedocs.io)
- **Code Coverage:** [Codecov Dashboard](https://app.codecov.io/gh/danielkorkin/loadcfg/)
- **GitHub Repository:** [github.com/danielkorkin/loadcfg](https://github.com/danielkorkin/loadcfg)
- **PyPI:** [pypi.org/project/loadcfg](https://pypi.org/project/loadcfg)

## Example Usage

```python
from loadcfg import LoadJson, LoadYaml, Template, ConfigValidationError

# --- Loading a configuration file ---
config = LoadJson("config.json")
print(config.name)          # Access via attribute notation.
print(config.info.age)

# --- Defining a configuration template ---
class ProgramConfig(Template):
    name: str
    age: int
    # You can also define nested templates:
    # details: OtherTemplate

# Validate a loaded configuration
try:
    ProgramConfig.validate(config)
except ConfigValidationError as err:
    print("Configuration error:", err)

# Alternatively, validate directly from the config instance:
config.validate(ProgramConfig)

# --- Generating an example configuration ---
example_json = ProgramConfig.generate(fmt="json")
print(example_json)

example_yaml = ProgramConfig.generate(fmt="yaml")
print(example_yaml)
```

## Testing

This library uses [pytest](https://docs.pytest.org) for testing. To run tests locally, use:

```bash
pytest
```

## Contributing

Contributions are encouraged and appreciated! Feel free to submit issues and pull requests on [GitHub](https://github.com/danielkorkin/loadcfg).

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

Maintained by Daniel Korkin (<daniel.d.korkin@gmail.com>)
