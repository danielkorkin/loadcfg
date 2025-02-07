Usage Example
=============

This guide demonstrates how to use **loadcfg** to load, validate, and generate configuration files in various formats.

Installation
------------

Install **loadcfg** from PyPI with:

.. code-block:: bash

    pip install loadcfg

Loading a Configuration File
----------------------------

### JSON

Load a JSON configuration file using:

.. code-block:: python

    from loadcfg import LoadJson

    config = LoadJson("config.json")
    print(config.name)          # Access values using dot-notation
    print(config.info.age)

### YAML

Load a YAML configuration file using:

.. code-block:: python

    from loadcfg import LoadYaml

    config = LoadYaml("config.yaml")
    print(config.name)
    print(config.value)

### TOML

Load a TOML configuration file using:

.. code-block:: python

    from loadcfg import LoadToml

    config = LoadToml("config.toml")
    print(config.name)
    print(config.value)

### INI

Load an INI configuration file using:

.. code-block:: python

    from loadcfg import LoadIni

    config = LoadIni("config.ini")
    # Note: Values in INI files are stored as strings.
    print(config.name)
    print(config.value)

Defining and Validating a Configuration Template
-------------------------------------------------

Define a configuration schema using the Template base class:

.. code-block:: python

    from loadcfg import Template, ConfigValidationError

    class ProgramConfig(Template):
        name: str
        age: int
        # You can also define nested templates:
        # details: OtherTemplate

Validate a configuration against the template:

.. code-block:: python

    try:
        ProgramConfig.validate(config)
    except ConfigValidationError as err:
        print("Configuration error:", err)

Alternatively, invoke validation directly on the configuration object:

.. code-block:: python

    config.validate(ProgramConfig)

Generating Example Configurations
-----------------------------------

Generate example configuration files in various formats:

.. code-block:: python

    # Generate JSON
    example_json = ProgramConfig.generate(fmt="json")
    print(example_json)

    # Generate YAML
    example_yaml = ProgramConfig.generate(fmt="yaml")
    print(example_yaml)

    # Generate TOML
    example_toml = ProgramConfig.generate(fmt="toml")
    print(example_toml)

    # Generate INI
    example_ini = ProgramConfig.generate(fmt="ini")
    print(example_ini)

Testing and Contributing
------------------------

To run the tests locally, use:

.. code-block:: bash

    pytest

Contributions are encouraged and appreciated. Please see the GitHub repository for details:

    https://github.com/danielkorkin/loadcfg

Documentation and Code Coverage
-------------------------------

- Full documentation is available at: https://loadcfg.readthedocs.io
- Code coverage details can be found at: https://app.codecov.io/gh/danielkorkin/loadcfg
