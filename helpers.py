

def register(key, destination_dict):
    """
    Decorator function that assigns the wrapped function to a key in the specified dictionary.
    """
    def decorator(func):
        destination_dict[key] = func
        return func
    return decorator