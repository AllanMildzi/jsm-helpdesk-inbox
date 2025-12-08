def extract_json_from_string(json: str) -> dict:
    opening_index = json.index('{')
    closing_index = json.rindex('}')

    return json[opening_index:closing_index+1]