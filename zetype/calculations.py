"""Miscellaneous calculation utility functions that serve multiple-purposes."""

import time


def minutes_since(start: float) -> float:
    """
    Calculate the number of minutes elapsed since a given start time.

    Args:
        start (float): The start time in seconds (typically obtained using time.time()).

    Returns:
        float: The number of minutes elapsed since the start time.
    """
    return (time.time() - start) / 60
