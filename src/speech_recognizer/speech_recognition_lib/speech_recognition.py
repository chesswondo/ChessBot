import re
from typing import Any, List
import speech_recognition as sr
from speech_recognizer.speech_recognizer_base import SpeechRecognizerBase

class SpeechRecognizerLib(SpeechRecognizerBase):
    '''Class for speech recognition using SpeechRecognition library.'''
    def __init__(self, config: dict) -> None:
        '''
        Initializes an instance of SpeechRecognizerLib.

        : param config: (dict) - main configuration object.
        
        : return: (None) - this function does not return any value.
        '''
        super().__init__(config)
        self._recognizer = sr.Recognizer()

    def record(self) -> Any:
        '''Records audio from micro.
        
        : return: (Any) - recorded audio.
        '''
        with sr.Microphone() as source:
            print("Listening...")
            audio = self._recognizer.listen(source)
        return audio

    def recognize(self, audio: Any) -> List[str]:
        '''Recognizes the given audio.
        
        : param audio: (Any) - recorded audio file.
        
        : return: (List[str]) - recognized text in it.'''
        try:
            text = self._recognizer.recognize_google(audio)
            pattern = r'[^a-zA-Z0-9]'
            text = re.sub(pattern, '', text).lower()
            print(f"You said: {text}")
            return [text]
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
        except sr.RequestError:
            print("Sorry, there was an error processing your request.")