SYSTEM_PROMPTS = {
    "Determine request type":
    """
    Here are available request types:
    {request_types}

    Which request type best matches the following user's email? 
    Return only the type id.
    """,

    "Determine request fields":
    """
    Fill the following form fields based on the following user's email.
    Requests Fields: {request_fields}
    Return valid JSON with the value of each fieldId as keys and the extracted value as values.
    Don't put keys with null or None or empty values.
    For the values, if validValues is empty, extract it from the email.
    Otherwise, choose from the list and set the value as a JSON object with "value" as the key and the label as its value.
    """
}