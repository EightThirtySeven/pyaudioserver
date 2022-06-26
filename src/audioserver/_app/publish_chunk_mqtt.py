import paho.mqtt.client as mqtt

from .._domain.publish_chunk import PublishChunk


class PublishChunkMQTT(PublishChunk):
    """A chunk publisher using Paho MQTT."""

    def __init__(self, client: mqtt.Client, site_id: str):
        """
        Args:
            client: The MQTT client.
        """
        super().__init__(site_id)
        self._client = client

    def execute(self, wav_bytes: bytes):
        self._client.publish(self._get_topic(), wav_bytes)
