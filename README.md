# loadcfg

Python Config Simply and Easily

## Example

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

# Alternatively, you can call validate on the loaded config:
config.validate(ProgramConfig)

# --- Generating an example configuration ---
example_json = ProgramConfig.generate(fmt="json")
print(example_json)

example_yaml = ProgramConfig.generate(fmt="yaml")
print(example_yaml)
```
