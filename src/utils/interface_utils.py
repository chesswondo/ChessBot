from enum import Enum

class ButtonValue(str, Enum):
    """
    Enumeration for button values.

    Possible values:
    - ButtonValue.BLACK: "black"
    - ButtonValue.WHITE: "white"
    - ButtonValue.SPEECH_RECOGNITION: "speech_recognition"
    - ButtonValue.AUTO_MODE: "auto_mode"
    - ButtonValue.DETECTION_MODE: "detection_mode"
    - ButtonValue.SUBMIT: "submit"
    """
    BLACK = "Black"
    WHITE = "White"

    SPEECH_RECOGNITION = "Speech recognition"
    AUTO_MODE = "Auto mode"
    DETECTION_MODE = "Detection mode"

    SUBMIT = "submit"

    def __eq__(self, other):
        return self.value == other

    def __hash__(self):
        return hash(self.value)

class LabelValue(str, Enum):
    """
    Enumeration for label values.

    Possible values:
    - LabelValue.COLOR_TITLE: "Choose the color"
    - LabelValue.COLOR_QUESTION: "What color do you play?"
    - LabelValue.MODE_TITLE: "Choose the mode"
    - LabelValue.MODE_QUESTION: "Choose the program mode"
    """
    COLOR_TITLE = "Choose the color"
    COLOR_QUESTION = "What color do you play?"
    MODE_TITLE = "Choose the mode"
    MODE_QUESTION = "Choose the program mode"

    def __eq__(self, other):
        return self.value == other

    def __hash__(self):
        return hash(self.value)