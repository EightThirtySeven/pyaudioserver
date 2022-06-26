import json
import logging
import os
from typing import Any

import coloredlogs
import paho.mqtt.client as mqtt

from ._app.player import PlaySoundPlayBytes
from ._app.publish_chunk_mqtt import PublishChunkMQTT
from ._app.record_chunks_sounddevice import RecordChunksSoundDevice

logger = logging.getLogger("audioserver")
coloredlogs.install(
    logger=logger, level=logging._nameToLevel[os.environ.get("LOG_LEVEL", "DEBUG")]
)


class Main:
    def __init__(self, site_id: str):
        self._client = mqtt.Client()
        self._play_bytes_topic = f"hermes/audioServer/{site_id}/playBytes/+"
        self._play_finished_topic = f"hermes/audioServer/{site_id}/playFinished"
        self._play_bytes = PlaySoundPlayBytes()
        self._record_chunks = RecordChunksSoundDevice(
            PublishChunkMQTT(self._client, site_id)
        )

        def on_connect(client: mqtt.Client, userdata: Any, flags: int, rc: int):
            """The connect handler."""
            client.subscribe(self._play_bytes_topic)
            logger.info(f"Connected to broker")
            logger.debug(f"Subscribed to {self._play_bytes_topic} (siteId = {site_id})")
            self._record_chunks.start()

        def on_message(client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage):
            """The message handler."""
            if msg.topic.startswith(self._play_bytes_topic.rsplit("/", 1)[0]):
                request_id = msg.topic.split("/")[-1]
                wav_bytes = msg.payload
                logger.debug(f"Received play bytes request {request_id}")

                def on_complete():
                    client.publish(
                        self._play_finished_topic, json.dumps({"id": request_id})
                    )

                self._play_bytes.execute(wav_bytes, on_complete)

        self._client.on_connect = on_connect
        self._client.on_message = on_message

    def loop_forever(self, host: str, port: int = 1883):
        """Loop forever.

        Args:
            endpoint: The MQTT broker endpoint.
        """
        self._client.connect(host, port)
        try:
            self._client.loop_forever()
        except KeyboardInterrupt:
            self._record_chunks.stop()
            self._play_bytes.shutdown()
