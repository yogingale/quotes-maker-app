"""AWS helper service."""

from dataclasses import dataclass, field

import boto3
from boto3 import resource


@dataclass
class AWS:
    """AWS client."""


@dataclass
class Rekognition(AWS):
    """Rekognition client."""

    region_name: str = "us-east-2"
    client: resource = field(init=False)

    def __post_init__(self):
        self.client = boto3.client(
            "rekognition",
            region_name=self.region_name,
        )

    def detect_labels(self, encoded_image: str) -> dict:
        """Detect labels AKA objects from encoded image."""
        return self.client.detect_labels(Image={"Bytes": encoded_image})
