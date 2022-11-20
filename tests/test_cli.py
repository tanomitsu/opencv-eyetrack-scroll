from src import cli


def test_say_hello():
    assert cli.say_hello() == "Hello, world!"

