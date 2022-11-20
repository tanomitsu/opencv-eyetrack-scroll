from src import cli
import cv2


def test_say_hello() -> None:
    assert cli.say_hello() == "Hello, world!"
