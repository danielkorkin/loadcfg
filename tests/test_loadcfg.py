import json

import pytest
import yaml

from loadcfg import Config, ConfigValidationError, LoadJson, LoadYaml, Template

# === Tests for Config class ===


def test_config_attribute_access():
    """Test that a Config instance supports attribute access recursively."""
    data = {"name": "Alice", "info": {"age": 30, "details": {"city": "Wonderland"}}}
    config = Config(data)
    assert config.name == "Alice"
    assert config.info.age == 30
    assert config.info.details.city == "Wonderland"


def test_config_set_attribute():
    """Test that setting an attribute via dot-notation updates the underlying dict."""
    config = Config({"a": 1})
    config.b = 2
    assert config["b"] == 2


def test_config_getattr_error():
    """Test that accessing a missing attribute raises AttributeError."""
    config = Config({"a": 1})
    with pytest.raises(AttributeError):
        _ = config.non_existent


def test_config_list_conversion():
    """Test that dictionaries inside lists are recursively converted to Config."""
    data = {"list": [{"key": "value"}]}
    config = Config(data)
    assert isinstance(config.list, list)
    assert isinstance(config.list[0], Config)
    assert config.list[0].key == "value"


def test_config_invalid_data():
    """Test that initializing a Config with a non-dictionary raises ValueError."""
    with pytest.raises(ValueError) as exc_info:
        Config("not a dict")
    assert "Config data must be a dictionary" in str(exc_info.value)


# === Tests for LoadJson ===


def test_load_json_valid(tmp_path):
    """Test loading a valid JSON configuration file."""
    data = {"name": "Test", "value": 123}
    file_path = tmp_path / "config.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")
    config = LoadJson(str(file_path))
    assert config.name == "Test"
    assert config.value == 123


def test_load_json_invalid(tmp_path):
    """Test that loading an invalid JSON file raises json.JSONDecodeError."""
    file_path = tmp_path / "bad.json"
    file_path.write_text("Not a JSON", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        _ = LoadJson(str(file_path))


def test_load_json_file_not_found(tmp_path):
    """Test that a non-existent JSON file raises FileNotFoundError."""
    file_path = tmp_path / "nonexistent.json"
    with pytest.raises(FileNotFoundError):
        _ = LoadJson(str(file_path))


# === Tests for LoadYaml ===


def test_load_yaml_valid(tmp_path):
    """Test loading a valid YAML configuration file."""
    data = {"name": "YAMLTest", "value": 456}
    file_path = tmp_path / "config.yaml"
    file_path.write_text(yaml.dump(data), encoding="utf-8")
    config = LoadYaml(str(file_path))
    assert config.name == "YAMLTest"
    assert config.value == 456


def test_load_yaml_invalid_structure(tmp_path):
    """
    Test that a YAML file with a non-dictionary top-level structure
    raises ValueError.
    """
    file_path = tmp_path / "bad.yaml"
    # Write a YAML string that represents a list (not a dict)
    file_path.write_text(yaml.dump([1, 2, 3]), encoding="utf-8")
    with pytest.raises(ValueError):
        _ = LoadYaml(str(file_path))


def test_load_yaml_invalid_yaml(tmp_path):
    """
    Test that a YAML file with invalid YAML syntax raises a yaml.YAMLError.
    """
    file_path = tmp_path / "invalid.yaml"
    file_path.write_text("key: [unbalanced brackets", encoding="utf-8")
    with pytest.raises(yaml.YAMLError):
        _ = LoadYaml(str(file_path))


# === Tests for Template functionality ===


# A dummy template for testing using type annotations.
class DummyTemplate(Template):
    name: str
    age: int


def test_template_validate_success():
    """Test that a valid config passes the template validation."""
    data = {"name": "Bob", "age": 25}
    config = Config(data)
    # Should not raise any exception.
    DummyTemplate.validate(config)


def test_template_validate_missing_field():
    """Test that a missing required field causes validation to fail."""
    data = {"name": "Bob"}  # 'age' is missing.
    config = Config(data)
    with pytest.raises(ConfigValidationError) as exc_info:
        DummyTemplate.validate(config)
    assert "Missing required field: 'age'" in str(exc_info.value)


def test_template_validate_wrong_type():
    """Test that a field with the wrong type causes validation to fail."""
    data = {"name": "Bob", "age": "not an int"}
    config = Config(data)
    with pytest.raises(ConfigValidationError) as exc_info:
        DummyTemplate.validate(config)
    assert "expected type 'int'" in str(exc_info.value)


# Testing nested templates.
class NestedTemplate(Template):
    value: int


class ParentTemplate(Template):
    name: str
    nested: NestedTemplate


def test_template_nested_validate_success():
    """Test that a nested template validates correctly when all fields are valid."""
    data = {"name": "Parent", "nested": {"value": 10}}
    config = Config(data)
    ParentTemplate.validate(config)


def test_template_nested_validate_failure():
    """Test that nested validation fails when a nested field is of the wrong type."""
    data = {"name": "Parent", "nested": {"value": "not an int"}}
    config = Config(data)
    with pytest.raises(ConfigValidationError) as exc_info:
        ParentTemplate.validate(config)
    assert "expected type 'int'" in str(exc_info.value)


def test_template_generate_json():
    """Test that generate(fmt='json') produces valid JSON with default example values."""
    generated = DummyTemplate.generate(fmt="json")
    # Validate that the generated string is valid JSON.
    data = json.loads(generated)
    assert "name" in data
    assert "age" in data
    # Default example values: str -> "example", int -> 0.
    assert data["name"] == "example"
    assert data["age"] == 0


def test_template_generate_yaml():
    """Test that generate(fmt='yaml') produces valid YAML with default example values."""
    generated = DummyTemplate.generate(fmt="yaml")
    # Validate that the generated string is valid YAML.
    data = yaml.safe_load(generated)
    assert "name" in data
    assert "age" in data
    assert data["name"] == "example"
    assert data["age"] == 0


def test_template_generate_invalid_format():
    """Test that calling generate with an unsupported format raises ValueError."""
    with pytest.raises(ValueError):
        DummyTemplate.generate(fmt="xml")


def test_config_instance_validate_method():
    """
    Test that the instance method validate() on a Config object correctly delegates
    to the provided Template's validate method.
    """
    data = {"name": "Alice", "age": 30}
    config = Config(data)
    # Should not raise error.
    config.validate(DummyTemplate)


# === Test for Template using class attributes instead of annotations ===


class AttrTemplate(Template):
    name = "default"
    age = 0


def test_template_with_attributes():
    """
    Test that a Template subclass defined with class attributes (instead of annotations)
    is handled properly.
    """
    data = {"name": "Alice", "age": 30}
    config = Config(data)
    # Validate using the template.
    AttrTemplate.validate(config)
    # Generate example config and verify default values.
    generated = AttrTemplate.generate(fmt="json")
    data_generated = json.loads(generated)
    assert data_generated["name"] == "example"  # From _get_example_value for str.
    assert data_generated["age"] == 0  # From _get_example_value for int.


# === Additional tests to cover _get_example_value branches ===


# Define a dummy type to represent an unknown type.
class UnknownType:
    pass


class AllTypesTemplate(Template):
    int_field: int
    float_field: float
    str_field: str
    bool_field: bool
    list_field: list
    dict_field: dict
    unknown_field: UnknownType


def test_all_types_template_generate():
    """
    Test that a template with fields of various types generates the expected default values.
    This covers:
      - int: returns 0
      - float: returns 0.0
      - str: returns "example"
      - bool: returns False
      - list: returns []
      - dict: returns {}
      - unknown types: returns None
    """
    generated = AllTypesTemplate.generate(fmt="json")
    data = json.loads(generated)
    assert data["int_field"] == 0
    assert data["float_field"] == 0.0
    assert data["str_field"] == "example"
    assert data["bool_field"] is False
    assert data["list_field"] == []
    assert data["dict_field"] == {}
    assert data["unknown_field"] is None
