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
        self.audio_name = config["audio_name"]+'.wav'
        self.model_name = config["model_name"]
        self.model_path = '../assets/models/speech_recognition/'+self.model_name
        self.model_params = config["model_parameters"]
        if os.path.exists(self.model_path):
            self.processor = WhisperProcessor.from_pretrained(self.model_path)
            self.model = WhisperForConditionalGeneration.from_pretrained(self.model_path)
        else:
            Path(self.model_path).mkdir(parents=True, exist_ok=True)
            self.processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
            self.processor.save_pretrained(self.model_path)

            self.model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")
            self.model.save_pretrained(self.model_path)

    def record(self) -> Any:
        '''Records audio from micro.
        
        : return: (string) - name of recorded audio.
        '''
        sample_rate = self.model_params["sample_rate"]
        duration = self.model_params["duration"]
        channels = self.model_params["channels"]
        record_audio(self.audio_name, duration=duration, sample_rate=sample_rate, channels=channels)
        return self.audio_name

    def recognize(self, audio: Any) -> List[str]:
        '''Recognizes the given audio.
        
        : param audio: (string) - name of recorded audio file.
        
        : return: (List[str]) - recognized text in it.
        '''
        num_beams   = self.model_params["num_beams"]
        max_length  = self.model_params["max_length"]
        sample_rate = self.model_params["sample_rate"]

        waveform, cur_sample_rate = torchaudio.load(self.audio_name)
        os.remove(self.audio_name)

        if cur_sample_rate != sample_rate:
            resampler = torchaudio.transforms.Resample(orig_freq=cur_sample_rate, new_freq=sample_rate)
            waveform = resampler(waveform)

        input_features = self.processor(waveform.squeeze().numpy(), sampling_rate=sample_rate, return_tensors="pt").input_features

        with torch.no_grad():
            generated_ids = self.model.generate(
                input_features,
                num_beams=num_beams,
                max_length=max_length,
                num_return_sequences=num_beams
            )

        transcriptions = list(self.processor.batch_decode(generated_ids, skip_special_tokens=True))
        pattern = r'[^a-zA-Z0-9]'
        for i in range(len(transcriptions)): 
            transcriptions[i] = re.sub(pattern, '', transcriptions[i]).lower()

        return transcriptions
