import io
import threading

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write as wav_write

from .._domain.publish_chunk import PublishChunk
from .._domain.record_chunks import RecordChunks


class RecordChunksSoundDevice(RecordChunks):
    def __init__(self, publish_chunk: PublishChunk):
        super().__init__(publish_chunk)
        self._sample_rate = 16000
        self._chunk_duration = 1
        self._shutdown = threading.Event()

        def streaming_thread(shutdown: threading.Event, publish_chunk: PublishChunk):
            """The streaming audio thread.

            Args:
                shutdown: The event to kill the recording thread.
                publish_chunk: The business logic for publishing an audio chunk.
            """
            while not shutdown.is_set():
                data = sd.rec(
                    int(self._chunk_duration * self._sample_rate),
                    samplerate=self._sample_rate,
                    channels=1,
                    dtype=np.int16,
                )
                sd.wait()
                with io.BytesIO() as file:
                    wav_write(file, self._sample_rate, data.astype(np.int16))
                    file.seek(0)
                    wav_bytes = file.read()
                    publish_chunk.execute(wav_bytes)

        self._thread = threading.Thread(
            target=streaming_thread, args=(self._shutdown, self._publish_chunk)
        )

    def start(self):
        self._thread.start()

    def stop(self):
        self._shutdown.set()
