class WaveWatch3Error(Exception):
    pass


class ChoiceError(WaveWatch3Error):
    def __init__(self, choice, choices):
        self._choice = choice
        self._choices = tuple(choices)

    def __str__(self):
        choices = ", ".join([repr(c) for c in self._choices])
        return f"{self._choice!r}: invalid choice (not one of {choices})"


class DateValueError(WaveWatch3Error):
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg
