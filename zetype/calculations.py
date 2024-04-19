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


def get_words_typed(characters_typed: int) -> float:
    """
    Estimate the number of words typed based on the number of characters typed.

    This function calculates the estimated number of words typed based on the
    average word length of 4.7 characters.

    Args:
        characters_typed (int): The total number of characters typed.

    Returns:
        float: The estimated number of words typed.
    """
    # TODO: Consider adding more accurate WPM tracking using real word count
    return characters_typed / 4.7


def get_accuracy(correct: int, total: int) -> float:
    """
    Calculate the accuracy percentage based on correct and total counts.

    Args:
        correct (int): The number of correctly typed characters.
        total (int): The total number of characters typed.

    Returns:
        float: The accuracy percentage (0 to 100).
    """
    if total == 0:
        return 0
    return (correct / total) * 100
