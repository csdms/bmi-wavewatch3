"""Exceptions raised from the *bmi_wavewatch3* package."""


class WaveWatch3Error(Exception):
    """Base exception for *bmi_wavewatch3* errors."""

    pass


class ChoiceError(WaveWatch3Error):
    """Raise this exceptions when an invalid choice is made."""

    def __init__(self, choice, choices):
        self._choice = choice
        self._choices = tuple(choices)

    def __str__(self):
        """Return the exception as a string."""
        choices = ", ".join([repr(c) for c in self._choices])
        return f"{self._choice!r}: invalid choice (not one of {choices})"


class DateValueError(WaveWatch3Error):
    """Raise this exception when an invalid date is encountered."""

    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        """Return the exception as a string."""
        return self._msg
