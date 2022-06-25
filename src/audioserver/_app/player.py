import tempfile
from os.path import join

from playsound import playsound

from .._domain.play_bytes import PlayBytes


class PlaySoundPlayBytes(PlayBytes):
    """An implementation of play bytes using `playsound`."""

    def execute(self, wav_data: bytes):
        with tempfile.TemporaryDirectory() as dir_name:
            temp_filename = join(dir_name, "chunk.wav")
            with open(temp_filename, "wb") as wav_file:
                wav_file.write(wav_data)
            playsound(temp_filename)
