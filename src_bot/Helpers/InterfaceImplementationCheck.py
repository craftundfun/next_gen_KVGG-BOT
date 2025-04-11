import inspect

from src_bot.Helpers.FunctionName import listenerName
from src_bot.Interface.Interface import Interface
from src_bot.Logging.Logger import Logger

logger = Logger("InterfaceImplementationCheck")


def checkInterfaceImplementation(func: callable, interface: type = Interface) -> bool:
    """
    Check if the given function is an instance of the given interface and asynchronous.

    :param func: The function to check
    :param interface: The interface to check against
    :return: True if the function is an instance of the interface, False otherwise
    """
    if not inspect.iscoroutinefunction(func):
        logger.warning(f"Function is not asynchronous: {listenerName(func)}")

        return False

    if not issubclass(func.__self__.__class__, interface):
        logger.warning(f"Function is not an instance of {interface.__class__}: {listenerName(func)}")

        return False

    logger.debug(f"Function is an instance of {interface.__class__}: {listenerName(func)}")

    return True
