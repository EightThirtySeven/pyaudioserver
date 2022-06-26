from abc import ABC
from typing import Callable


class PlayBytes(ABC):
    def execute(self, wav_data: bytes, on_complete: Callable[[], None]):
        """Play bytes of a WAV file (non-blocking).

        Args:
            wav_data: Bytes formatted as a valid WAV file.
            on_complete: The callback for when the bytes finish playing.
        """
        pass
