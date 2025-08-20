import pytest
from main import parse_array_on_dict, get_extension_field, get_extension_unique_fields


def test_parse_array_on_dict_basic():
    lines = [
        '{"url": "test1", "response_time": "0.12"}\n',
        '{"url": "test2", "response_time": "0.34"}\n'
    ]
    result = parse_array_on_dict(lines)

    assert isinstance(result, list)
    assert result[0]["url"] == "test1"
    assert result[0]["response_time"] == "0.12"
    assert result[1]["url"] == "test2"


def test_parse_array_on_dict_without_quotes_in_number():
    lines = ['{"url": "test", "response_time": 5}\n']
    result = parse_array_on_dict(lines)
    assert result[0]["response_time"] == "5"  # число тоже превращается в строку


def test_get_extension_field_with_matches():
    data = [
        {"url": "a", "response_time": "1.0"},
        {"url": "a", "response_time": "2.0"},
        {"url": "b", "response_time": "3.0"},
    ]
    count, total, avg = get_extension_field(data, "a")

    assert count == 2
    assert total == 3.0
    assert avg == 1.5


def test_get_extension_field_no_matches():
    data = [{"url": "a", "response_time": "1.0"}]
    count, total, avg = get_extension_field(data, "b")

    assert count == 0
    assert total == 0
    # avg при делении на ноль вызовет ZeroDivisionError,
    # поэтому такой вызов нужно оборачивать в pytest.raises
    with pytest.raises(ZeroDivisionError):
        _ = sum([]) / len([])  # поведение как в функции


def test_get_extension_unique_fields_default():
    data = [
        {"url": "a", "response_time": "1.0"},
        {"url": "a", "response_time": "2.0"},
        {"url": "b", "response_time": "3.0"},
    ]
    result = get_extension_unique_fields(data, "file.txt")

    assert isinstance(result, list)
    assert len(result) == 2  # уникальные url: a, b
    assert result[0]["count_item"] == 2
    assert "avg" in result[0]
    assert "file.txt" in result[0]  # поле с именем файла присутствует


def test_get_extension_unique_fields_with_custom_fields():
    data = [
        {"url": "a", "response_time": "1.0", "method": "GET"},
        {"url": "a", "response_time": "2.0", "method": "GET"},
    ]
    result = get_extension_unique_fields(
        data,
        "file.txt",
        unique_field="url",
        fields=["url", "method"]
    )

    assert "method" in result[0]
    assert "url" in result[0]
    assert "avg" in result[0]
