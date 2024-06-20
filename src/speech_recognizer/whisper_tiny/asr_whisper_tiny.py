import os
import re
import torch
import torchaudio
from pathlib import Path
from typing import Any, List
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from utils.speech_recognition_utils import record_audio
from speech_recognizer.speech_recognizer_base import SpeechRecognizerBase

class SpeechRecognizerWhisper(SpeechRecognizerBase):
    '''Class for speech recognition using OpenAI whisper-tiny speech recognition model.'''
    def __init__(self, config: dict) -> None:
        '''
        Initializes an instance of SpeechRecognizerWhisper.

        : param config: (dict) - main configuration object.
        
        : return: (None) - this function does not return any value.
        '''
        super().__init__(config)
        self._audio_name = config["audio_name"]+'.wav'
        self._model_name = config["model_name"]
        self._model_path = '../assets/models/speech_recognition/'+self._model_name
        self._model_params = config["model_parameters"]
        if os.path.exists(self._model_path):
            self._processor = WhisperProcessor.from_pretrained(self._model_path)
            self._model = WhisperForConditionalGeneration.from_pretrained(self._model_path)
        else:
            Path(self._model_path).mkdir(parents=True, exist_ok=True)
            self._processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
            self._processor.save_pretrained(self._model_path)

            self._model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")
            self._model.save_pretrained(self._model_path)

    def record(self) -> Any:
        '''Records audio from micro.
        
        : return: (string) - name of recorded audio.
        '''
        sample_rate = self._model_params["sample_rate"]
        duration = self._model_params["duration"]
        channels = self._model_params["channels"]
        record_audio(self._audio_name, duration=duration, sample_rate=sample_rate, channels=channels)
        return self._audio_name

    def recognize(self, audio: Any) -> List[str]:
        '''Recognizes the given audio.
        
        : param audio: (string) - name of recorded audio file.
        
        : return: (List[str]) - recognized text in it.
        '''
        num_beams   = self._model_params["num_beams"]
        max_length  = self._model_params["max_length"]
        sample_rate = self._model_params["sample_rate"]

        waveform, cur_sample_rate = torchaudio.load(self._audio_name)
        os.remove(self._audio_name)

        if cur_sample_rate != sample_rate:
            resampler = torchaudio.transforms.Resample(orig_freq=cur_sample_rate, new_freq=sample_rate)
            waveform = resampler(waveform)

        input_features = self._processor(waveform.squeeze().numpy(), sampling_rate=sample_rate, return_tensors="pt").input_features

        with torch.no_grad():
            generated_ids = self._model.generate(
                input_features,
                num_beams=num_beams,
                max_length=max_length,
                num_return_sequences=num_beams
            )

        transcriptions = list(self._processor.batch_decode(generated_ids, skip_special_tokens=True))
        pattern = r'[^a-zA-Z0-9]'
        for i in range(len(transcriptions)): 
            transcriptions[i] = re.sub(pattern, '', transcriptions[i]).lower()

        return transcriptions
