from urllib.parse import urlencode


def set_query_params(response, **kwargs):
    """
    Set (GET) query parameters for response. NOTE: This function does not support multiple calls for single response.
    :param response: Response object where parameters are added
    :param kwargs: Parameters to add
    :return: Response with parameters added (parameters are added in-place, however)
    """
    params = "?" + urlencode(kwargs)
    response["Location"].rstrip()
    response["Location"] += params
    return response
