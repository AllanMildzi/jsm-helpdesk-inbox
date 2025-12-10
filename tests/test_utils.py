from src.utils import extract_json_from_string

def test_extract_json_from_string():
    # Test case 1: Valid JSON string
    text_with_json = "Some text before {\"key\": \"value\", \"number\": 123} some text after."
    expected_json = "{\"key\": \"value\", \"number\": 123}"
    assert extract_json_from_string(text_with_json) == expected_json

    # Test case 2: JSON at the beginning of the string
    text_with_json_start = "{\"key\": \"value\", \"number\": 123} some text after."
    expected_json_start = "{\"key\": \"value\", \"number\": 123}"
    assert extract_json_from_string(text_with_json_start) == expected_json_start

    # Test case 3: JSON at the end of the string
    text_with_json_end = "Some text before {\"key\": \"value\", \"number\": 123}"
    expected_json_end = "{\"key\": \"value\", \"number\": 123}"
    assert extract_json_from_string(text_with_json_end) == expected_json_end

    # Test case 4: Nested JSON (should extract the outermost)
    nested_json = "Text {\"outer\": {\"inner\": 1}} more text"
    expected_nested_json = "{\"outer\": {\"inner\": 1}}"
    assert extract_json_from_string(nested_json) == expected_nested_json

    # Test case 5: Empty JSON object
    empty_json_string = "Some text {} other text"
    expected_empty_json = "{}"
    assert extract_json_from_string(empty_json_string) == expected_empty_json
