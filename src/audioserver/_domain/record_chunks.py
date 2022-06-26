from abc import ABC

from .publish_chunk import PublishChunk


class RecordChunks(ABC):
    """An interface for a chunk recording service."""

    def __init__(self, publish_chunk: PublishChunk):
        """
        Args:
            publish_chunk: The business logic for publishing a chunk.
        """
        self._publish_chunk = publish_chunk

    def start(self):
        """Start recording WAV chunks."""
        pass

    def stop(self):
        """Stop recording WAV chunks."""
        pass
