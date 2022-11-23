from pynput.mouse import Controller

mouse = Controller()


def scroll(x: int, y: int) -> None:
    mouse.scroll(x, y)
    return


def get_move(diff: int) -> int:
    def f(x: int) -> int:
        if abs(x) == 0:
            return 0
        e = x // abs(x)
        if abs(x) < 10:
            return 0
        elif abs(x) < 3000:
            return 1 * e
        else:
            return (abs(x) - 9) * e

    return f(diff)
