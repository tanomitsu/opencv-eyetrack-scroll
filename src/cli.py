import cv2


def say_hello() -> str:
    return "Hello, world!"


def main() -> None:
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            # qキーを押したら終了
            break
    cap.release()
    cv2.destroyAllWindows()
