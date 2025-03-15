"""Module for main entrypoint."""


def foo() -> str:  # pylint: disable=disallowed-name
    """
    Method to be executed in module entrypoint.

    ...

    -------
    Returns
    -------
    String for local test.
    """
    return "bar"


if __name__ == "__main__":
    foo()
