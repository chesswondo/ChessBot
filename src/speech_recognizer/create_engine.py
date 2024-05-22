from speech_recognizer.speech_recognizer_base import SpeechRecognizerBase
from speech_recognizer.speech_recognition_lib.speech_recognition import SpeechRecognizerLib
from utils.common_utils import load_config

def create_speech_recognition_engine(config: dict) -> SpeechRecognizerBase:
    '''
    Creates an instance of the speech recognition engine based on config.
    
    : param config: (dict) - main config file.
    
    : return: (SpeechRecognizerBase) - instance of the speech recognition engine.
    '''

    if config["speech_recognition"]["recognition_type"] == "speech_recognition":
        recognition_config = load_config('../assets/configs/speech_recognition/speech_recognition/config.json')
        return SpeechRecognizerLib(recognition_config)