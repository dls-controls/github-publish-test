# Possible future states (for internal use).
RUNNING = 'RUNNING'
#  Task has set the return or exception and this future is filled
FINISHED = 'FINISHED'

_FUTURE_STATES = [
    RUNNING,
    FINISHED
]


class Error(Exception):
    """Base class for all future-related exceptions."""
    # TODO: for review - user-defined exceptions - should we use them?
    pass


class TimeoutError(Error):
    """The operation exceeded the given deadline."""
    pass


class RemoteError(Error):
    """The remote operation generated an error."""
    pass


class Future(object):
    """Represents the result of an asynchronous computation.
       This class has a similar API to concurrent.futures.Future but this
       simpler version is not thread safe"""

    def __init__(self, task):
        """Initializes the future """
        self._task = task
        self._state = RUNNING
        self._result = None
        self._exception = None

    def done(self):
        """Return True if the future finished executing."""
        return self._state in [FINISHED]

    def __get_result(self):
        if self._exception:
            raise RemoteError(self._exception)
        else:
            return self._result

    def result(self, timeout=None):
        """Return the result of the call that the future represents.

        Args:
            timeout: The number of seconds to wait for the result if the future
                isn't done. If None, then there is no limit on the wait time.

        Returns:
            The result of the call that the future represents.

        Raises:
            TimeoutError: If the future didn't finish executing before the given
                timeout.
            Exception: If the call raised then that exception will be raised.
        """
        if self._state == FINISHED:
            return self.__get_result()

        self._task.wait_all(self, timeout)

        return self.__get_result()

    def exception(self, timeout=None):
        """Return the exception raised by the call that the future represents.

        Args:
            timeout: The number of seconds to wait for the exception if the
                future isn't done. If None, then there is no limit on the wait
                time.

        Returns:
            The exception raised by the call that the future represents or None
            if the call completed without raising.

        Raises:
            TimeoutError: If the future didn't finish executing before the given
                timeout.
        """

        if self._state == FINISHED:
            return self._exception

        self._task.wait_all(self, timeout)

        return self._exception

    # The following methods should only be used by Task and in unit tests.

    def set_result(self, result):
        """Sets the return value of work associated with the future.

        Should only be used by Task and unit tests.
        """
        self._result = result
        self._state = FINISHED

    def set_exception(self, exception):
        """Sets the result of the future as being the given exception.

        Should only be used by Task and unit tests.
        """
        self._exception = exception
        self._state = FINISHED
