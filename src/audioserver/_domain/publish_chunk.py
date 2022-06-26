from abc import ABC


class PublishChunk(ABC):
    def __init__(self, site_id: str):
        """
        Args:
            site_id: The site id.
        """
        self._site_id = site_id

    def _get_topic(self):
        """Get the pub/sub topic for the chunk publishing."""
        return f"hermes/audioServer/{self._site_id}/audioFrame"

    def execute(self, wav_bytes: bytes):
        """Publish the WAV chunk."""
        pass
