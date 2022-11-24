# Third Party Library
import cv2
import dlib

# First Party Library
from src.mouse.scroll import get_move, scroll

# Local Library
from .color import bgr_red
from .eye.eye_detect import extract_eyes, get_contouring, get_eye_center
from .face.face_detect import get_face_mid, get_one_face
from .type import Point

"""
landmarks:
    右目: [36, 37, 38, 39, 40, 41]
    左目: [42, 43, 44, 45, 46, 47]
    中心線: [27, 28, 29, 30]
"""
predictor = dlib.shape_predictor("data/shape_68.dat")

right_indices = list(range(36, 42))
left_indices = list(range(42, 48))
center_indices = list(range(27, 31))


def do_nothing(_) -> None:
    pass


def main() -> None:
    threshold = 30
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("display")
    while True:
        # fps測定
        tick = cv2.getTickCount()
        ret, frame = cap.read()
        if ret is False:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = get_one_face(gray_frame)

        display = frame.copy()

        if face is not None:
            landmarks = predictor(gray_frame, face)

            r_points: list[Point] = []
            l_points: list[Point] = []
            c_points: list[Point] = []
            for ri in right_indices:
                r_points.append(
                    Point(landmarks.part(ri).x, landmarks.part(ri).y)
                )
            for li in left_indices:
                l_points.append(
                    Point(landmarks.part(li).x, landmarks.part(li).y)
                )
            for ci in center_indices:
                c_points.append(
                    Point(landmarks.part(ci).x, landmarks.part(ci).y)
                )

            rc: Point = get_eye_center(r_points)
            lc: Point = get_eye_center(l_points)
            cv2.circle(display, rc.to_tuple(), 2, bgr_red, -1)
            cv2.circle(display, lc.to_tuple(), 2, bgr_red, -1)
            face_mid_x = get_face_mid(l_points, r_points, display)

            eyes_frame = extract_eyes(frame, l_points, r_points)

            # gray scale for thresholding
            eyes_frame_gray = cv2.cvtColor(eyes_frame, cv2.COLOR_BGR2GRAY)

            # threshold
            _, thresh = cv2.threshold(
                eyes_frame_gray, threshold, 255, cv2.THRESH_BINARY
            )
            thresh_erode = cv2.erode(thresh, None, iterations=2)
            thresh_dilate = cv2.dilate(thresh_erode, None, iterations=4)
            thresh_blur = cv2.medianBlur(thresh_dilate, 3)
            thresh_inv = cv2.bitwise_not(thresh_blur)

            # get the contouring
            r_cnt_res = get_contouring(
                thresh_inv[:, :face_mid_x], face_mid_x, display, is_right=False
            )
            l_cnt_res = get_contouring(
                thresh_inv[:, face_mid_x:], face_mid_x, display, is_right=True
            )
            l_diff: Point
            r_diff: Point
            if l_cnt_res is not None:
                l_eye_center = l_cnt_res
                l_diff = l_eye_center - lc
                print(f"Left: {l_diff}")
            else:
                l_diff = Point(0, 0)
            if r_cnt_res is not None:
                r_eye_center = r_cnt_res
                r_diff = r_eye_center - rc
                print(f"Right: {r_diff}")
            else:
                r_diff = Point(0, 0)
            total_diff = l_diff + r_diff
            scroll(0, -get_move(total_diff.x))

        fps = cv2.getTickFrequency() / (cv2.getTickCount() - tick)
        print(f"fps: {fps}")
        cv2.imshow("display", display)
        if cv2.waitKey(50) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
