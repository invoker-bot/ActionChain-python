from typing import *
from typing import Any, Optional
from tenacity import *
from tenacity.stop import stop_base
from abc import ABCMeta, abstractmethod
from datetime import timedelta


T = TypeVar('T')
time_unit_type = Union[int, float, timedelta]


def to_seconds(time_unit: time_unit_type) -> float:
    return float(time_unit.total_seconds() if isinstance(time_unit, timedelta) else time_unit)

def is_none_or_true(value: Optional[bool]) -> bool:
    return value is None or value

def is_none_or_false(value: Optional[bool]) -> bool:
    return value is None or not value


class condition_stop(stop_base):

    def __init__(self, condition, context) -> None:
        self.condition = condition
        self.context = context

    def __call__(self, retry_state: "RetryCallState") -> bool:
        return is_none_or_false(self.condition(self.context))


class BaseAction(Generic[T], metaclass=ABCMeta):
    """BaseAction is an abstract class that represents an action.

    An action is a single unit of work that can be executed.
    """

    def condition(self, context: T) -> Optional[bool]:
        """Check if the action can be executed.

        Args:
            context: The context to pass to the condition.

        Returns:
            True if the action can be executed, False otherwise, and None if the condition is not defined.
        """
        return None

    def condition_noexcept(self, context: T) -> Optional[bool]:
        """Check if the action can be executed.

        Args:
            context: The context to pass to the condition.

        Returns:
            True if the action can be executed, False otherwise.
        """
        try:
            return self.condition(context)
        except Exception:
            return False

    @abstractmethod
    def execute(self, context: T):
        """Execute the action.

        Args:
            context: The context to pass to the action.
        """
        pass

    def __call__(self, context: T, retry: BaseRetrying = None) -> Any:
        if retry is not None:
            retry.wait |= condition_stop(self.condition, context)
        if is_none_or_true(self.condition(context)):
            if retry is None:
                self.execute(context)
            else:
                retry(self.execute, context)
        return self.result(context)
    
    def result(self, context: T) -> Optional[bool]:
        """Get the result of the execution.

        Args:
            context: The context to pass to the result.

        Returns:
            True if the action was executed successfully, False otherwise, and None if the result is not defined.
        """
        return None

    def result_noexcept(self, context: T) -> Optional[bool]:
        """Get the result of the execution.

        Args:
            context: The context to pass to the result.

        Returns:
            True if the action was executed successfully, False otherwise.
        """
        try:
            return self.result(context)
        except Exception:
            return False


class FunctionalAction(BaseAction):
    """FunctionalAction is an action that executes a function.

    Args:
        func: The function to execute.
        condition: The condition to check before executing the function.
        result: The result to return after executing the function.
    """
    def __init__(self, fn: Callable[[T], None], condition: Callable[[T], Optional[bool]] = lambda _: None, result: Callable[[T], Optional[bool]] = lambda _: None):
        self.fn = fn
        self.condition = condition
        self.result = result

    def execute(self, context: T):
        """Execute the function.

        Args:
            context: The context to pass to the function.
        """
        self.fn(context)



class ActionSequentialChain(BaseAction[T]):
    """ActionChain is an abstract class that represents a chain of actions.

    An action chain is a sequence of actions that are executed in order.
    """
    def __init__(self, *args: BaseAction[T]):
        """Initialize the action chain."""
        self.actions = list(args)

    def condition(self, context: T) -> Optional[bool]:
        value = False
        for action in self.actions:
            result = action.condition(context)
            if result is None:
                value = None
            elif result:
                return True
        return value

    def execute(self, context: T):
        """Execute the action chain.

        Args:
            context: The context to pass to the action chain.
        """
        for action in self.actions:
            action(context)

    def result(self, context: T) -> Optional[bool]:
        if len(self.actions) > 0:
            return self.actions[-1].result(context)

class ActionPallelChain(BaseAction[T]):
    """ActionChain is an abstract class that represents a chain of actions.

    An action chain is a sequence of actions that are executed in order.
    """
    def __init__(self, *args: BaseAction[T]):
        """Initialize the action chain."""
        self.actions = list(args)

    def condition(self, context: T) -> Optional[bool]:
        value = False
        for action in self.actions:
            result = action.condition(context)
            if result is None:
                value = None
            elif result:
                return True
        return value

    def execute(self, context: T):
        """Execute the action chain.

        Args:
            context: The context to pass to the action chain.
        """
        for action in self.actions:
            action(context)

    def result(self, context: T) -> Optional[bool]:
        if len(self.actions) > 0:
            return self.actions[-1].result(context)