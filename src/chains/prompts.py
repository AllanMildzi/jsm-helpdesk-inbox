SYSTEM_PROMPTS = {
    "Determine request type":
    """
    Here are available request types:
    {request_types}

    Which request type best matches the following user's email? 
    Return only the type id.
    If you can't determine the request type, return -1.
    """,

    "Determine request fields":
    """
    Fill the following form fields based on the following user's email.
    Requests Fields: {request_fields}
    Return valid JSON with the value of each fieldId as keys.

    For the fieldIds that have an empty validValues list, extract the value from the email.
    For the fieldIds that have a non-empty validValues list (components and customfield_xxxxx), select the most appropriate label, not the value.
    If you can't determine a value, select the first valid value.
    Don't include the `attachment` key.
    
    If you can't extract any fields, return an empty JSON object: {{}}
    If there are missing fields, return those fields only.
    """
}