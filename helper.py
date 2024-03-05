def has_unsupported_params(url, supported_params=[]):
    """function to check if URL contains unsupported parameters"""
    return (
        len([param for param in url["query_params"] if param not in supported_params])
        > 0
    )


def missing_fields(request_body, required_fields):
    """function to find and return a list of missing fields from a request body"""
    return [field for field in required_fields if field not in request_body]
