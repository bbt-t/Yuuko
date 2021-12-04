import json
from pathlib import Path
import subprocess

from vosk import Model, KaldiRecognizer

from loader import logger_guru




@logger_guru.catch()
def recognize_locally(name_file: str) -> str:
    """
    We recognize the voice locally.
    ATTENTION! choosing the full vosk-model will result in very high memory consumption!
    :param name_file: name voice message file
    :return: what recognized
    """
    sample_rate: int = 16000
    model = Model("vosk_model_ru_lite")
    rec = KaldiRecognizer(model, sample_rate)
    process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i',
                                name_file,
                                '-ar', str(sample_rate), '-ac', '1', '-f', 's16le', '-'],
                               stdout=subprocess.PIPE)
    while True:
        data = process.stdout.read(4000)
        if len(data) == 0:
            break
        rec.AcceptWaveform(data)

    path = Path(name_file)
    path.unlink()
    return json.loads(rec.FinalResult())['text']
