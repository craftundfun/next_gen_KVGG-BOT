def listenerName(function: callable) -> str:
    """
    Get the name of a function or return "Unknown" if the name is not available

    :param function: Callable function
    :return:
    """
    return getattr(function, "__name__", "Unknown") + "@" + getattr(function, "__module__", "Unknown")
