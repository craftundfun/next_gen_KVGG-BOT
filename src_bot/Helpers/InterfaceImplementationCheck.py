import inspect

from src_bot.Helpers.FunctionName import listenerName
from src_bot.Interface.Interface import Interface
from src_bot.Logging.Logger import Logger

logger = Logger("InterfaceImplementationCheck")


def checkInterfaceImplementation(func: callable, interface: type = Interface) -> None | Exception:
    """
    Check if the given function is an instance of the given interface and asynchronous.

    :param func: The function to check
    :param interface: The interface to check against
    :return: Nothing if the function is implementing the interface, otherwise raises an error
    """
    if not inspect.iscoroutinefunction(func):
        logger.warning(f"Function is not asynchronous: {listenerName(func)}")

        raise ValueError(f"Function is not asynchronous: {listenerName(func)}")

    if not issubclass(func.__self__.__class__, interface):
        logger.warning(f"Function is not an instance of {interface.__class__}: {listenerName(func)}")

        raise NotImplementedError(f"Function is not an instance of {interface.__name__}: {listenerName(func)}")

    if not hasattr(interface, func.__name__):
        logger.warning(f"Function is not an instance of {interface.__class__}: {listenerName(func)}")

        raise NotImplementedError(f"Function is not given in {interface.__name__}: {listenerName(func)}")
