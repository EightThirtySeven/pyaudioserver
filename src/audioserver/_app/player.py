from dataclasses import dataclass
import tempfile
from os.path import join
from typing import Callable

from playsound import playsound

from .._domain.play_bytes import PlayBytes
import queue
import threading


@dataclass
class PlayWavChunk:
    data: bytes
    on_complete: Callable[[], None]


class PlaySoundPlayBytes(PlayBytes):
    """An implementation of play bytes using `playsound`."""

    def __init__(self):
        def playback_thread(wav_queue: queue.Queue, shutdown: threading.Event):
            """
            Args:
                wav_queue: A queue of WAV chunks.
                shutdown: A shutdown event.
            """
            while not shutdown.is_set():
                if not wav_queue.empty():
                    chunk = wav_queue.get()
                    with tempfile.TemporaryDirectory() as dir_name:
                        temp_filename = join(dir_name, "chunk.wav")
                        with open(temp_filename, "wb") as wav_file:
                            wav_file.write(chunk.data)
                        playsound(temp_filename, block=True)
                        chunk.on_complete()

        self._wav_queue = queue.Queue()
        self._shutdown = threading.Event()

        threading.Thread(
            target=playback_thread, args=(self._wav_queue, self._shutdown)
        ).start()

    def execute(self, wav_data: bytes, on_complete: Callable[[], None]):
        self._wav_queue.put(PlayWavChunk(wav_data, on_complete))

    def shutdown(self):
        """Kill the playback thread."""
        self._shutdown.set()
