from abc import ABC


class PlayBytes(ABC):
    def execute(self, wav_data: bytes):
        """Play bytes of a WAV file.
        
        Args:
            wav_data: Bytes formatted as a valid WAV file.
        """
        pass
