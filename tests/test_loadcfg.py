import configparser
import json
import os

import pytest
import toml
import yaml

from loadcfg import (Config, ConfigValidationError, LoadIni, LoadJson,
                     LoadToml, LoadYaml, Template)

# === Tests for Config class ===


def test_config_attribute_access():
    data = {"name": "Alice", "info": {"age": 30, "details": {"city": "Wonderland"}}}
    config = Config(data)
    assert config.name == "Alice"
    assert config.info.age == 30
    assert config.info.details.city == "Wonderland"


def test_config_set_attribute():
    config = Config({"a": 1})
    config.b = 2
    assert config["b"] == 2


def test_config_getattr_error():
    config = Config({"a": 1})
    with pytest.raises(AttributeError):
        _ = config.non_existent


def test_config_list_conversion():
    data = {"list": [{"key": "value"}]}
    config = Config(data)
    assert isinstance(config.list, list)
    assert isinstance(config.list[0], Config)
    assert config.list[0].key == "value"


def test_config_invalid_data():
    with pytest.raises(ValueError) as exc_info:
        Config("not a dict")
    assert "Config data must be a dictionary" in str(exc_info.value)


# === Tests for LoadJson ===


def test_load_json_valid(tmp_path):
    data = {"name": "Test", "value": 123}
    file_path = tmp_path / "config.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")
    config = LoadJson(str(file_path))
    assert config.name == "Test"
    assert config.value == 123


def test_load_json_invalid(tmp_path):
    file_path = tmp_path / "bad.json"
    file_path.write_text("Not a JSON", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        _ = LoadJson(str(file_path))


def test_load_json_file_not_found(tmp_path):
    file_path = tmp_path / "nonexistent.json"
    with pytest.raises(FileNotFoundError):
        _ = LoadJson(str(file_path))


# === Tests for LoadYaml ===


def test_load_yaml_valid(tmp_path):
    data = {"name": "YAMLTest", "value": 456}
    file_path = tmp_path / "config.yaml"
    file_path.write_text(yaml.dump(data), encoding="utf-8")
    config = LoadYaml(str(file_path))
    assert config.name == "YAMLTest"
    assert config.value == 456


def test_load_yaml_invalid_structure(tmp_path):
    file_path = tmp_path / "bad.yaml"
    file_path.write_text(yaml.dump([1, 2, 3]), encoding="utf-8")
    with pytest.raises(ValueError):
        _ = LoadYaml(str(file_path))


def test_load_yaml_invalid_yaml(tmp_path):
    file_path = tmp_path / "invalid.yaml"
    file_path.write_text("key: [unbalanced brackets", encoding="utf-8")
    with pytest.raises(yaml.YAMLError):
        _ = LoadYaml(str(file_path))


# === Tests for LoadToml ===


def test_load_toml_valid(tmp_path):
    data = {"name": "TomlTest", "value": 789}
    file_path = tmp_path / "config.toml"
    file_path.write_text(toml.dumps(data), encoding="utf-8")
    config = LoadToml(str(file_path))
    assert config.name == "TomlTest"
    assert config.value == 789


def test_load_toml_invalid_structure(tmp_path):
    """Test that a TOML file with a top-level array raises ValueError."""
    file_path = tmp_path / "bad.toml"
    # A top-level array; toml.loads should return a list.
    file_path.write_text("[1, 2, 3]", encoding="utf-8")
    with pytest.raises(ValueError):
        _ = LoadToml(str(file_path))


def test_load_toml_file_not_found(tmp_path):
    file_path = tmp_path / "nonexistent.toml"
    with pytest.raises(FileNotFoundError):
        _ = LoadToml(str(file_path))


# === Tests for LoadIni ===


def test_load_ini_valid(tmp_path):
    ini_content = """
[DEFAULT]
name = IniTest
value = 321

[section]
key = subvalue
"""
    file_path = tmp_path / "config.ini"
    file_path.write_text(ini_content, encoding="utf-8")
    config = LoadIni(str(file_path))
    assert config.name == "IniTest"
    assert config.value == "321"  # INI files store values as strings.
    assert "section" in config
    assert config.section["key"] == "subvalue"


def test_load_ini_file_not_found(tmp_path):
    file_path = tmp_path / "nonexistent.ini"
    with pytest.raises(FileNotFoundError):
        _ = LoadIni(str(file_path))


# === Tests for Template functionality ===


class DummyTemplate(Template):
    name: str
    age: int


def test_template_validate_success():
    data = {"name": "Bob", "age": 25}
    config = Config(data)
    DummyTemplate.validate(config)


def test_template_validate_missing_field():
    data = {"name": "Bob"}
    config = Config(data)
    with pytest.raises(ConfigValidationError) as exc_info:
        DummyTemplate.validate(config)
    assert "Missing required field: 'age'" in str(exc_info.value)


def test_template_validate_wrong_type():
    data = {"name": "Bob", "age": "not an int"}
    config = Config(data)
    with pytest.raises(ConfigValidationError) as exc_info:
        DummyTemplate.validate(config)
    assert "expected type 'int'" in str(exc_info.value)


class NestedTemplate(Template):
    value: int


class ParentTemplate(Template):
    name: str
    nested: NestedTemplate


def test_template_nested_validate_success():
    data = {"name": "Parent", "nested": {"value": 10}}
    config = Config(data)
    ParentTemplate.validate(config)


def test_template_nested_validate_failure():
    data = {"name": "Parent", "nested": {"value": "not an int"}}
    config = Config(data)
    with pytest.raises(ConfigValidationError) as exc_info:
        ParentTemplate.validate(config)
    assert "expected type 'int'" in str(exc_info.value)


def test_template_generate_json():
    generated = DummyTemplate.generate(fmt="json")
    data = json.loads(str(generated))
    assert "name" in data
    assert "age" in data
    assert data["name"] == "example"
    assert data["age"] == 0


def test_template_generate_yaml():
    generated = DummyTemplate.generate(fmt="yaml")
    data = yaml.safe_load(str(generated))
    assert "name" in data
    assert "age" in data
    assert data["name"] == "example"
    assert data["age"] == 0


def test_template_generate_toml():
    generated = DummyTemplate.generate(fmt="toml")
    data = toml.loads(str(generated))
    assert "name" in data
    assert "age" in data
    assert data["name"] == "example"
    assert data["age"] == 0


def test_template_generate_ini():
    generated = DummyTemplate.generate(fmt="ini")
    parser = configparser.ConfigParser()
    parser.read_string(str(generated))
    default_values = list(parser["DEFAULT"].values())
    assert "example" in default_values or "0" in default_values


def test_template_generate_invalid_format():
    with pytest.raises(ValueError):
        DummyTemplate.generate(fmt="xml")


def test_config_instance_validate_method():
    data = {"name": "Alice", "age": 30}
    config = Config(data)
    config.validate(DummyTemplate)


class AttrTemplate(Template):
    name = "default"
    age = 0


def test_template_with_attributes():
    data = {"name": "Alice", "age": 30}
    config = Config(data)
    AttrTemplate.validate(config)
    generated = AttrTemplate.generate(fmt="json")
    data_generated = json.loads(str(generated))
    assert data_generated["name"] == "example"
    assert data_generated["age"] == 0


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
    generated = AllTypesTemplate.generate(fmt="json")
    data = json.loads(str(generated))
    assert data["int_field"] == 0
    assert data["float_field"] == 0.0
    assert data["str_field"] == "example"
    assert data["bool_field"] is False
    assert data["list_field"] == []
    assert data["dict_field"] == {}
    assert data["unknown_field"] is None


# === Tests for GeneratedConfig .save() feature ===

import os


@pytest.mark.parametrize(
    "fmt,ext",
    [
        ("json", "json"),
        ("yaml", "yaml"),
        ("toml", "toml"),
        ("ini", "ini"),
    ],
)
def test_generated_config_save(tmp_path, fmt, ext):
    generated = DummyTemplate.generate(fmt=fmt)
    filename = tmp_path / f"output.{ext}"
    returned_filename = generated.save(str(filename))
    assert os.path.basename(returned_filename) == f"output.{ext}"
    assert os.path.isfile(returned_filename)
    with open(returned_filename, "r", encoding="utf-8") as f:
        saved_content = f.read()
    assert saved_content == str(generated)


def test_generated_config_save_default_filename(tmp_path):
    generated = DummyTemplate.generate(fmt="json")
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        returned_filename = generated.save()  # No filename provided.
        assert returned_filename == "config.json"
        assert os.path.isfile("config.json")
        with open("config.json", "r", encoding="utf-8") as f:
            content = f.read()
        assert content == str(generated)
    finally:
        os.chdir(old_cwd)
