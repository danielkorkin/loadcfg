Usage Example
=============

This guide demonstrates how to use **loadcfg** to load, validate, and generate configuration files in various formats—and how to save the generated configuration to a file.

Installation
------------

Install **loadcfg** from PyPI with:

.. code-block:: bash

    pip install loadcfg

Loading a Configuration File
----------------------------

JSON
~~~~

Load a JSON configuration file using:

.. code-block:: python

    from loadcfg import LoadJson

    config = LoadJson("config.json")
    print(config.name)          # Access values using dot-notation
    print(config.info.age)

YAML
~~~~

Load a YAML configuration file using:

.. code-block:: python

    from loadcfg import LoadYaml

    config = LoadYaml("config.yaml")
    print(config.name)
    print(config.value)

TOML
~~~~

Load a TOML configuration file using:

.. code-block:: python

    from loadcfg import LoadToml

    config = LoadToml("config.toml")
    print(config.name)
    print(config.value)

INI
~~~

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

Generating and Saving Example Configurations
----------------------------------------------

You can generate example configuration files in various formats and save them directly to a file.

.. code-block:: python

    # Generate a JSON example configuration and print it.
    example_json = ProgramConfig.generate(fmt="json")
    print(example_json)
    # Save the generated configuration to "test.json".
    example_json.save("test.json")
    # If no filename is provided, the default will be "config.<fmt>" (e.g. "config.json").

    # Similarly, generate and save YAML, TOML, or INI formats:
    example_yaml = ProgramConfig.generate(fmt="yaml")
    example_yaml.save("test.yaml")

    example_toml = ProgramConfig.generate(fmt="toml")
    example_toml.save("test.toml")

    example_ini = ProgramConfig.generate(fmt="ini")
    example_ini.save("test.ini")

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
