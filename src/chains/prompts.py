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
    Return valid JSON with the value of each fieldId as keys.
    For the values, if validValues is an empty list, extract it from the email.
    Otherwise, choose the most appropriate value from validValues as a JSON object.
    If you can't determine a value, select the first valid value.
    Don't put keys with null or None or empty values.
    """
}