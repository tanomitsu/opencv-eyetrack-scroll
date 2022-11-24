# Third Party Library
import cv2
import dlib

# First Party Library
from src.color import bgr_black
from src.type import Mat, Point

face_detector = dlib.get_frontal_face_detector()


def get_one_face(gray_image: Mat) -> Mat | None:
    faces = face_detector(gray_image)
    if len(faces) == 0:
        return None
    face = faces[0]

    return face


# returns the y-value of the face's mid from points
def get_face_mid(
    lps: list[Point], rps: list[Point], frame: Mat | None = None
) -> int:
    if frame is not None:
        cv2.circle(
            frame,
            ((lps[0].x + rps[3].x) // 2, (lps[0].y + rps[3].y) // 2),
            4,
            bgr_black,
            2,
        )
    return (lps[0].x + rps[3].x) // 2
