from pynput.mouse import Controller

mouse = Controller()


def scroll(x: int, y: int) -> None:
    mouse.scroll(x, y)
    return
