# Third Party Library
import cv2

# First Party Library
from src import cli


def test_say_hello() -> None:
    assert cli.say_hello() == "Hello, world!"
